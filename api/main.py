from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.webhooks import router as webhook_router
from api.workflows import router as workflow_router
from api.runs import router as runs_router
from api.plugins import router as plugin_router

from core.database import DatabaseManager
from core.logger import get_logger
from api.ai import router as ai_router
from api.plugins import router as plugin_router
from api.templates import router as templates_router


# ---------------------------
# LOGGER + DATABASE
# ---------------------------

logger = get_logger("api")
db = DatabaseManager(logger)


# ---------------------------
# FASTAPI APP
# ---------------------------

app = FastAPI(
    title="WorkflowOS",
    version="1.0.0",
    description="Distributed Job Processing Engine"
)


# ---------------------------
# CORS (IMPORTANT FOR BUILDER)
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # production me domain restrict karna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# ROUTERS
# ---------------------------

app.include_router(router)
app.include_router(webhook_router)
app.include_router(workflow_router)
app.include_router(runs_router)
app.include_router(plugin_router)
app.include_router(ai_router)
app.include_router(plugin_router)
app.include_router(templates_router)


# ---------------------------
# ROOT
# ---------------------------

@app.get("/")
def root():
    return {
        "service": "WorkflowOS",
        "status": "running"
    }


# ---------------------------
# HEALTH CHECK
# ---------------------------

@app.get("/health")
def health():

    try:

        with db._connect() as conn:
            return {
                "status": "healthy",
                "database": "connected"
            }

    except Exception:

        return {
            "status": "error",
            "database": "disconnected"
        }


# ---------------------------
# METRICS
# ---------------------------

@app.get("/metrics")
def metrics():

    return db.get_metrics()