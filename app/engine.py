from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .models import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    RunStateResponse,
    ExecutionStep,
    NodeConfig,
)
from .tools import get_tool


class Graph:
    def __init__(self, graph_id: UUID, definition: GraphCreateRequest) -> None:
        self.id = graph_id
        self.definition = definition


class Run:
    def __init__(self, run_id: UUID, graph: Graph, initial_state: Dict[str, Any]) -> None:
        self.id = run_id
        self.graph = graph
        self.state: Dict[str, Any] = dict(initial_state)
        self.current_node: Optional[str] = graph.definition.start_node
        self.log: list[ExecutionStep] = []


class GraphEngine:
    def __init__(self) -> None:
        self.graphs: Dict[UUID, Graph] = {}
        self.runs: Dict[UUID, Run] = {}

    # ------------------ GRAPH MANAGEMENT ------------------

    def create_graph(self, req: GraphCreateRequest) -> GraphCreateResponse:
        graph_id = uuid4()
        graph = Graph(graph_id, req)
        self.graphs[graph_id] = graph
        return GraphCreateResponse(graph_id=graph_id)

    # ------------------ RUN EXECUTION ---------------------

    def start_and_run(self, req: GraphRunRequest) -> GraphRunResponse:
        graph = self.graphs.get(req.graph_id)
        if not graph:
            raise ValueError("Graph not found")

        run = Run(uuid4(), graph, req.initial_state)
        self.runs[run.id] = run

        self._execute(run)

        return GraphRunResponse(
            run_id=run.id,
            final_state=run.state,
            log=run.log,
        )

    def get_run_state(self, run_id: UUID) -> RunStateResponse:
        run = self.runs.get(run_id)
        if not run:
            raise ValueError("Run not found")

        return RunStateResponse(
            run_id=run.id,
            current_node=run.current_node,
            state=run.state,
            log=run.log,
        )

    # ----------------- CONDITION CHECKER --------------------

    def _check_condition(self, state: Dict[str, Any], key: str, op: str, value: Any) -> bool:
        left = state.get(key)

        if op == "<": return left < value
        if op == "<=": return left <= value
        if op == ">": return left > value
        if op == ">=": return left >= value
        if op == "==": return left == value
        if op == "!=": return left != value

        return False

    # ----------------- MAIN EXECUTION LOOP -----------------

    def _execute(self, run: Run) -> None:
        steps = 0
        max_steps = 200  # safety

        while run.current_node is not None and steps < max_steps:
            steps += 1

            node_name = run.current_node
            node_cfg = run.graph.definition.nodes.get(node_name)

            if not node_cfg:
                break

            # 1. RUN TOOL
            tool_fn = get_tool(node_cfg.name)
            new_state = tool_fn(run.state)
            run.state.update(new_state)

            # 2. LOG STATE
            run.log.append(
                ExecutionStep(
                    node=node_name,
                    state_snapshot=dict(run.state)
                )
            )

            # 3. LOOP IF CONDITION MET
            if node_cfg.loop_while:
                cond = node_cfg.loop_while
                if self._check_condition(run.state, cond.key, cond.op, cond.value):
                    continue  # repeat same node

            # 4. BRANCHING (IF/ELSE)
            branch_taken = False
            for cond in node_cfg.branches:
                if self._check_condition(run.state, cond.key, cond.op, cond.value):
                    run.current_node = cond.next
                    branch_taken = True
                    break

            if branch_taken:
                continue

            # 5. DEFAULT NEXT NODE
            run.current_node = node_cfg.next


# Global engine instance
engine = GraphEngine()
