🚀 WorkflowOS

AI-Native Workflow Automation Engine (n8n Alternative)

WorkflowOS is a modular, plugin-based automation platform that allows you to build, execute, and scale workflows using APIs, webhooks, and AI-powered logic.

---

⚡ Features

- 🔌 Plugin-based architecture (install & extend easily)
- 🔄 Event-driven workflow engine
- 🌐 Webhook + REST API support
- 🧠 AI-ready system (future integration)
- 📊 Execution logs & monitoring
- 🧩 Modular node system (Triggers, Actions, Logic, Data)

---

🧱 Project Structure

workflowos/
│
├── api/            # FastAPI routes (webhooks, plugins, health)
├── engine/         # Workflow execution engine
├── plugins/        # Custom plugin system
├── core/           # Core utilities & logic
├── app/            # App-level orchestration
├── dashboard/      # UI (future / optional)
├── templates/      # Prebuilt workflows
├── agent/          # AI agent system (future)
├── marketplace/    # Plugin marketplace (future)

---

🔌 Plugin System

Each plugin follows a simple interface:

def run(data: dict):
    return {"status": "success"}

Example Plugins:

- "http_request"
- "save_db"
- "send_email"

---

⚙️ How It Works

1. Workflow is triggered (via webhook/API)
2. Nodes are executed sequentially
3. Each node loads its plugin dynamically
4. Plugin runs inside sandbox
5. Results are stored and returned

---

🚀 Getting Started

1. Clone repo

git clone https://github.com/mohsinakramchandia91-bit/workflowos.git
cd workflowos

2. Setup environment

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3. Run server

uvicorn api.main:app --reload

---

🔗 API Endpoints

Endpoint| Description
"/webhook/{workflow_id}"| Trigger workflow
"/plugins"| List plugins
"/health"| Health check
"/metrics"| System metrics

---

🧠 Roadmap

Phase 1 (Current)

- ✅ Plugin system
- ✅ Workflow execution engine
- ✅ Webhook triggers

Phase 2

- 🔄 DAG-based execution
- 🔄 Retry & error handling
- 🔄 Logging system upgrade

Phase 3

- 🧠 AI nodes (OpenAI, Claude)
- 💬 Chat-based workflow builder
- 📊 Visual dashboard

Phase 4

- 🌍 Marketplace
- 🔐 API key management
- 💰 SaaS deployment

---

🔥 Vision

Build a lightweight, AI-native alternative to n8n that is:

- Faster ⚡
- Smarter 🧠
- More flexible 🔧

---

👨‍💻 Author

Muhammad Mohsin

---

⭐ Support

If you like this project:

- ⭐ Star the repo
- 🍴 Fork it
- 🚀 Build on top of it

---
