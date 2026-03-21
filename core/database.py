import uuid
import psycopg2
from psycopg2.extras import Json
from core.config import POSTGRES_CONFIG


class DatabaseManager:
    def __init__(self, logger):
        self.logger = logger
        self._init_db()

    # ================= CONNECTION =================

    def _connect(self):
        return psycopg2.connect(**POSTGRES_CONFIG)

    # ================= INIT =================

    def _init_db(self):

        with self._connect() as conn:
            cur = conn.cursor()

            # workers
            cur.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id TEXT PRIMARY KEY,
                last_heartbeat TIMESTAMP
            );
            """)

            # jobs
            cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                tenant_id TEXT,
                plugin TEXT,
                status TEXT,
                priority INTEGER DEFAULT 5,
                progress INTEGER DEFAULT 0,
                message TEXT,
                result TEXT,
                error TEXT,
                created TIMESTAMP DEFAULT NOW(),
                started_at TIMESTAMP,
                finished TIMESTAMP,
                worker_id TEXT,
                retries INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3,
                timeout INTEGER DEFAULT 30,
                execution_time INTEGER DEFAULT 0
            );
            """)

            # workflows
            cur.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id SERIAL PRIMARY KEY,
                name TEXT,
                definition JSONB,
                created TIMESTAMP DEFAULT NOW()
            );
            """)

            # 🔥 NEW TABLES
            cur.execute("""
            CREATE TABLE IF NOT EXISTS workflow_runs (
                id SERIAL PRIMARY KEY,
                workflow_id INT,
                status TEXT,
                input JSONB,
                output JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS node_runs (
                id SERIAL PRIMARY KEY,
                workflow_run_id INT,
                node_id INT,
                status TEXT,
                input JSONB,
                output JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            conn.commit()

    # ================= STATE MACHINE =================

    VALID_TRANSITIONS = {
        "PENDING": ["RUNNING"],
        "RUNNING": ["COMPLETED", "FAILED"],
        "FAILED": ["PENDING"],
        "COMPLETED": []
    }

    def _validate_transition(self, job_id, new_status):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT status FROM jobs WHERE id=%s",
                (job_id,)
            )

            row = cur.fetchone()

            if not row:
                raise Exception("Job not found")

            current_status = row[0]

            allowed = self.VALID_TRANSITIONS.get(current_status, [])

            if new_status not in allowed:
                raise Exception(
                    f"Invalid state transition: {current_status} -> {new_status}"
                )

    # ================= WORKER =================

    def register_worker(self):

        worker_id = str(uuid.uuid4())

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO workers (id, last_heartbeat)
                VALUES (%s, NOW())
            """, (worker_id,))

            conn.commit()

        return worker_id

    def update_heartbeat(self, worker_id):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                UPDATE workers
                SET last_heartbeat = NOW()
                WHERE id = %s
            """, (worker_id,))

            conn.commit()

    def cleanup_dead_workers(self):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM workers
                WHERE last_heartbeat IS NOT NULL
                AND last_heartbeat < NOW() - INTERVAL '30 seconds'
            """)

            conn.commit()

    # ================= JOB =================

    def add_job(self, plugin_name, tenant_id="default", priority=5):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO jobs (tenant_id, plugin, status, priority)
                VALUES (%s, %s, 'PENDING', %s)
                RETURNING id
            """, (tenant_id, plugin_name, priority))

            job_id = cur.fetchone()[0]
            conn.commit()

            return job_id

    def get_job(self, job_id):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, plugin, status, result, error, created, finished
                FROM jobs
                WHERE id=%s
            """, (job_id,))

            row = cur.fetchone()

            if not row:
                return None

            return {
                "id": row[0],
                "plugin": row[1],
                "status": row[2],
                "result": row[3],
                "error": row[4],
                "created": row[5],
                "finished": row[6]
            }

    # ================= WORKFLOW =================

    def create_workflow(self, name, definition):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO workflows (name, definition)
                VALUES (%s, %s)
                RETURNING id
            """, (name, Json(definition)))

            workflow_id = cur.fetchone()[0]
            conn.commit()

            return workflow_id

    def list_workflows(self):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, name, created
                FROM workflows
                ORDER BY created DESC
            """)

            rows = cur.fetchall()

            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "created": r[2]
                }
                for r in rows
            ]

    # ================= WORKFLOW RUN LOGS =================

    def create_workflow_run(self, workflow_id, input_data):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO workflow_runs (workflow_id, status, input)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (workflow_id, "running", Json(input_data)))

            run_id = cur.fetchone()[0]
            conn.commit()

            return run_id

    def update_workflow_run(self, run_id, status, output):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                UPDATE workflow_runs
                SET status=%s, output=%s
                WHERE id=%s
            """, (status, Json(output), run_id))

            conn.commit()

    def create_node_run(self, workflow_run_id, node_id, status, input_data, output):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO node_runs (workflow_run_id, node_id, status, input, output)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                workflow_run_id,
                node_id,
                status,
                Json(input_data),
                Json(output)
            ))

            conn.commit()

    # ================= METRICS =================

    def get_metrics(self):

        with self._connect() as conn:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM jobs")
            total = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM jobs WHERE status='PENDING'")
            pending = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM jobs WHERE status='RUNNING'")
            running = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM jobs WHERE status='COMPLETED'")
            completed = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM jobs WHERE status='FAILED'")
            failed = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM workers")
            workers = cur.fetchone()[0]

            cur.execute("""
                SELECT COALESCE(AVG(execution_time),0)
                FROM jobs
                WHERE status='COMPLETED'
            """)

            avg_time = cur.fetchone()[0]

            return {
                "total_jobs": total,
                "pending_jobs": pending,
                "running_jobs": running,
                "completed_jobs": completed,
                "failed_jobs": failed,
                "worker_count": workers,
                "avg_execution_time_seconds": float(avg_time)
            }