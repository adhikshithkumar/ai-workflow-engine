from typing import Dict, Any, List
from .tools import register_tool


# 1. Split text into chunks
def split_text_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("text", "")
    chunk_size = int(state.get("chunk_size_words", 80))

    words = text.split()
    chunks: List[str] = []

    current: List[str] = []
    count = 0

    for word in words:
        if count >= chunk_size:
            chunks.append(" ".join(current))
            current = [word]
            count = 1
        else:
            current.append(word)
            count += 1

    if current:
        chunks.append(" ".join(current))

    return {"chunks": chunks}


# 2. Generate summary for each chunk
def generate_summaries_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    chunks: List[str] = state.get("chunks", [])
    summary_size = int(state.get("summary_chunk_words", 20))

    summaries = []
    for chunk in chunks:
        words = chunk.split()
        snippet = " ".join(words[:summary_size])
        summaries.append(snippet)

    return {"chunk_summaries": summaries}


# 3. Merge all summaries into one string
def merge_summaries_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    summaries: List[str] = state.get("chunk_summaries", [])
    merged = ". ".join(summaries)

    return {
        "summary": merged,
        "summary_length": len(merged),
    }


# 4. Refine summary based on character limit
def refine_summary_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    summary = state.get("summary", "")
    limit = int(state.get("summary_limit", 400))

    if len(summary) <= limit:
        return {"summary": summary, "summary_length": len(summary)}

    # Trim in a loop until it fits the limit
    current = summary
    while len(current) > limit:
        trimmed = current[:limit]
        last_space = trimmed.rfind(" ")
        if last_space != -1:
            trimmed = trimmed[:last_space]
        current = trimmed

    return {"summary": current, "summary_length": len(current)}


# Register all tools when app starts
def register_workflow_tools():
    register_tool("split_text", split_text_tool)
    register_tool("generate_summaries", generate_summaries_tool)
    register_tool("merge_summaries", merge_summaries_tool)
    register_tool("refine_summary", refine_summary_tool)
