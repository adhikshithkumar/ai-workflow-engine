✨ Mini Workflow Engine (FastAPI)

A lightweight, extensible workflow/agent execution engine built using FastAPI, supporting graph-based execution, state transitions, and custom tool integration.
This project was built as part of an assignment to demonstrate how multi-step logic can be automated using a workflow graph.

🚀 Features

✔ Graph-based workflow execution

✔ Each node represents a "tool" (function)

✔ Automatic state passing between nodes

✔ Logging of each node’s execution

✔ Example: Text Summarization Workflow

✔ Clean FastAPI routes to create, run, and inspect workflows

✔ Deployed API (Render)

✔ Well-structured Python project

📁 Project Structure
ai-workflow-engine/
│
├── app/
│   ├── main.py              # FastAPI app + default workflow
│   ├── engine.py            # Core workflow engine
│   ├── models.py            # Pydantic models for graph, runs, state
│   ├── tools.py             # Functions (tools) used in workflow
│   ├── workflows.py         # Registers tools + example workflow
│
├── requirements.txt         # Dependencies
├── Procfile                 # Deployment config
└── README.md                # Documentation

🧠 How the Workflow Engine Works
1. Workflow = Graph

Each workflow is modeled as a graph:

Nodes = steps (tools)

Edges = which step comes next

State = shared dict passed across steps

Example nodes:

split_text

generate_summaries

merge_summaries

refine_summary

2. Engine Execution Flow

1️⃣ Pick start node
2️⃣ Execute its tool
3️⃣ Update the shared state
4️⃣ Jump to next node
5️⃣ Repeat until node.next = None

The engine logs each step.

📌 Default Summarization Workflow

Runs four steps:

split_text

generate_summaries

merge_summaries

refine_summary

Produces:

chunks

intermediate summaries

a final refined summary

⚡ API Endpoints (FastAPI)
📌 Create a workflow

POST /graph/create

📌 Run a workflow

POST /graph/run

📌 Get run state

GET /graph/state/{run_id}

📌 Simplified summarization endpoint

POST /summarize

🧪 Example Output

Sample final result from /summarize endpoint:

{
  "summary": "FastAPI is a modern, fast web framework for building APIs with Python.",
  "summary_length": 70
}

🛠 How to Run Locally
1. Clone the repo
git clone https://github.com/adhikshithkumar/ai-workflow-engine.git
cd ai-workflow-engine

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Start the server
uvicorn app.main:app --reload

5. Open documentation
http://127.0.0.1:8000/docs

🌐 Live Deployment (Render)

API is deployed here:

👉 https://ai-workflow-engine.onrender.com/docs

🧩 What I Would Improve with More Time

Add persistent storage for graphs and runs

Add async background task support

Add user-defined workflows via UI

Support branching workflows (IF/ELSE logic)

Add authentication for multi-user use

Add tool registry with plugin system

Add visualization of execution graph