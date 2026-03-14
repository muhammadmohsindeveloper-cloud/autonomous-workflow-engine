# WorkflowOS

Open Source Automation Engine for Developers

WorkflowOS is a distributed automation platform that allows developers to build workflow pipelines, trigger tasks via webhooks, and execute plugins in a scalable environment.

---

## Features

- Workflow DAG Engine
- Plugin System
- Webhook Triggers
- Distributed Workers
- Job Queue
- Metrics API
- Docker Deployment
- Visual Workflow Builder

---

## Architecture

Client → API → Workflow Engine → Job Queue → Worker → Plugin

---

## Installation

Clone repository

git clone https://github.com/mohsinakramchandia91-bit/workflowos

cd workflowos

Start with Docker

docker compose up

Open API Docs

http://localhost:8000/docs

---

## Example Workflow

Webhook trigger executes plugins:

send_email  
save_db

---

## API Endpoints

GET /workflows  
POST /workflows  
POST /webhook/{workflow_id}  
GET /runs  
GET /metrics  

---

## Roadmap

- Visual workflow editor
- Plugin marketplace
- Multi-tenant support
- Cloud deployment
- Authentication

---

## License

MIT License