🚀 Mini Workflow Engine

A lightweight FastAPI-based workflow engine that lets you define multi-step graphs, manage state transitions, run agents, and observe step-by-step execution.

This project demonstrates a clean, modular implementation of a workflow engine suitable for automating AI agents, pipelines, and multi-step logic.

📂 Project Structure
ai-workflow-engine/
│
├── app/
│   ├── main.py          # FastAPI app + routes + startup events
│   ├── engine.py        # Core workflow engine (state machine, step runner)
│   ├── models.py        # Pydantic request/response models
│   ├── tools.py         # Custom tools/functions used by workflow steps
│   ├── workflows.py     # Registered workflows (summarization example)
│
├── requirements.txt     # Dependencies
├── Procfile             # Deployment config (Render/Railway)
└── README.md            # This file

✨ Features
🔹 1. Graph-based Workflow Engine

Supports:

Nodes

Directed transitions

State passing

Logging execution history

🔹 2. Clean FastAPI Endpoints
Method	Endpoint	Description
POST	/graph/create	Create a new workflow graph
POST	/graph/run	Run a workflow
GET	/graph/state/{run_id}	Retrieve execution state
POST	/summarize	Example agent workflow
🔹 3. Built-in Summarization Workflow

Demonstrates:

Splitting text into chunks

Generating chunk summaries

Merging summaries

Refining final summary

Returning execution log

🔹 4. Deployment Ready

Works on Render, Railway, or any cloud platform using:

web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

🛠️ How to Run Locally
1. Clone the repo
git clone https://github.com/<your-username>/ai-workflow-engine.git
cd ai-workflow-engine

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Start the server
uvicorn app.main:app --reload

5. Visit API Docs

Swagger UI:
👉 http://127.0.0.1:8000/docs

🧪 Example Run
Create a graph
POST /graph/create
{
  "name": "summarization_workflow"
}

Run it
POST /graph/run
{
  "graph_id": "<ID>",
  "text": "Your long text here…"
}

Get state
GET /graph/state/<run_id>

🌟 What I Would Improve With More Time
🔧 Engine Enhancements

Add conditional branches

Add parallel node execution

Add async tool execution

Improve logging with timestamps

📡 API Improvements

Add /health endpoint

Add /workflows to list registered graphs

🚀 Advanced Features (future)

WebSockets for real-time state updates

Integrating OpenAI / LLM-based tools

Background task scheduling

🎯 Evaluation Notes

This implementation focuses on:

Clear code structure

Readable engine logic

Simple state model

Good API practices

Step-by-step logged execution

Optional features are intentionally kept minimal since clarity matters more than complexity.