from typing import Any, Dict, List, Optional, Literal
from uuid import UUID
from pydantic import BaseModel


class NodeConfig(BaseModel):
    name: str
    next: Optional[str] = None

    class Branch(BaseModel):
        key: str
        op: Literal["<", "<=", ">", ">=", "==", "!="]
        value: Any
        next: str

    branches: List[Branch] = []
    loop_while: Optional[Branch] = None


class GraphCreateRequest(BaseModel):
    name: str
    start_node: str
    nodes: Dict[str, NodeConfig]


class GraphCreateResponse(BaseModel):
    graph_id: UUID


class GraphRunRequest(BaseModel):
    graph_id: UUID
    initial_state: Dict[str, Any]


class ExecutionStep(BaseModel):
    node: str
    state_snapshot: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: UUID
    final_state: Dict[str, Any]
    log: List[ExecutionStep]


class RunStateResponse(BaseModel):
    run_id: UUID
    current_node: Optional[str]
    state: Dict[str, Any]
    log: List[ExecutionStep]
