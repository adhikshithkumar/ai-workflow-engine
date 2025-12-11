from fastapi import FastAPI, HTTPException
from uuid import UUID

from .engine import engine
from .models import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    RunStateResponse,
    NodeConfig
)
from .workflows import register_workflow_tools


app = FastAPI(title="Mini Workflow Engine")


@app.on_event("startup")
def on_startup():
    """
    Runs once when the server starts.
    Registers tools and creates a default summarization graph.
    """
    register_workflow_tools()

    # Create default workflow graph
    default_graph = GraphCreateRequest(
        name="summarization_workflow",
        start_node="split_text",
        nodes={
            "split_text": NodeConfig(name="split_text", next="generate_summaries"),
            "generate_summaries": NodeConfig(name="generate_summaries", next="merge_summaries"),
            "merge_summaries": NodeConfig(name="merge_summaries", next="refine_summary"),
            "refine_summary": NodeConfig(name="refine_summary", next=None),
        },
    )

    # Save graph ID
    response = engine.create_graph(default_graph)
    app.state.default_graph_id = response.graph_id
    print("Default workflow graph created with ID:", response.graph_id)


# ------------------ GRAPH APIs ------------------

@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(req: GraphCreateRequest):
    return engine.create_graph(req)


@app.post("/graph/run", response_model=GraphRunResponse)
def run_graph(req: GraphRunRequest):
    try:
        return engine.start_and_run(req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
def state(run_id: UUID):
    try:
        return engine.get_run_state(run_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ------------------ SIMPLE SUMMARIZATION ENDPOINT ------------------

from pydantic import BaseModel
from typing import Any, Dict


class SummarizeRequest(BaseModel):
    text: str
    chunk_size_words: int = 80
    summary_chunk_words: int = 20
    summary_limit: int = 400


@app.post("/summarize", response_model=GraphRunResponse)
def summarize(req: SummarizeRequest):
    """
    Uses the default summarization workflow graph.
    """
    graph_id = app.state.default_graph_id

    initial_state: Dict[str, Any] = {
        "text": req.text,
        "chunk_size_words": req.chunk_size_words,
        "summary_chunk_words": req.summary_chunk_words,
        "summary_limit": req.summary_limit,
    }

    run_request = GraphRunRequest(
        graph_id=graph_id,
        initial_state=initial_state
    )

    return engine.start_and_run(run_request)
