"""
Orchestrator — coordinates all agents for a single chat turn.

Flow:
  Planner → (CSV Analysis + RAG) in parallel → Visualization → Knowledge Fusion → Insight
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime

from app.repositories.dataset_repository import dataset_repo
from app.repositories.document_repository import document_repo

from app.agents import planner_agent, csv_analysis_agent, visualization_agent, rag_agent
from app.agents import knowledge_fusion_agent, insight_agent
from app.services.chart_service import save_chart


async def run_pipeline(
    workspace_id: str,
    question: str,
    conversation_id: str,
    history: list[dict],
) -> dict:
    trace: dict = {"steps": [], "started_at": str(datetime.utcnow())}

    # 1. Build workspace file inventory for the Planner
    datasets = await dataset_repo.find_by_workspace(workspace_id)
    documents = await document_repo.find_by_workspace(workspace_id)

    file_inventory = [
        {
            "id": d["_id"],
            "filename": d["original_filename"],
            "kind": "dataset",
            "type": d["file_type"],
            "columns": d.get("columns", []),
            "status": d["preprocessing_status"],
        }
        for d in datasets
        if d["preprocessing_status"] == "complete"
    ] + [
        {
            "id": d["_id"],
            "filename": d["filename"],
            "kind": "document",
            "type": d["file_type"],
            "status": d["embedding_status"],
        }
        for d in documents
        if d["embedding_status"] == "complete"
    ]

    # 2. Planner Agent
    plan = await planner_agent.plan(question, file_inventory, history)
    trace["steps"].append({"agent": "planner", "result": plan})

    # 3. Resolve file paths / metadata
    csv_paths = _resolve_csv_paths(datasets, plan["csv_file_ids"])
    doc_meta = _resolve_doc_meta(documents, plan["doc_file_ids"])

    # 4. CSV Analysis + RAG in parallel
    csv_task = asyncio.to_thread(
        csv_analysis_agent.analyse,
        csv_paths,
        question,
        plan["query_type"],
    )
    rag_task = asyncio.to_thread(
        rag_agent.retrieve_context,
        list(doc_meta.keys()),
        doc_meta,
        question,
    )
    csv_summary, rag_result = await asyncio.gather(csv_task, rag_task)
    trace["steps"].append({"agent": "csv_analysis", "datasets": len(csv_paths)})
    trace["steps"].append({"agent": "rag", "chunks": len(rag_result.get("chunks", []))})

    # 5. Visualization Agent (only when Planner requested a chart)
    chart_info = None
    chart_response = None
    if plan["needs_chart"] and csv_paths:
        chart_info = await asyncio.to_thread(
            visualization_agent.generate_chart,
            csv_paths,
            question,
            plan.get("chart_hint", ""),
        )
        if chart_info:
            chart_id = await save_chart(
                workspace_id=workspace_id,
                message_id="pending",  # updated after message is saved
                chart_type=chart_info["chart_type"],
                title=chart_info["title"],
                plotly_json=chart_info["plotly_json"],
                image_path=chart_info.get("image_path", ""),
            )
            chart_info["id"] = chart_id
            chart_response = {
                "id": chart_id,
                "chart_type": chart_info["chart_type"],
                "title": chart_info["title"],
                "plotly_json": chart_info["plotly_json"],
                "image_url": f"/storage/charts/{chart_id}.png" if chart_info.get("image_path") else None,
            }
        trace["steps"].append({"agent": "visualization", "chart_type": chart_info.get("chart_type") if chart_info else None})

    # 6. Knowledge Fusion Agent
    fused_context = knowledge_fusion_agent.fuse(
        question=question,
        history=history,
        plan=plan,
        csv_summary=csv_summary,
        rag_result=rag_result,
        chart_info=chart_info,
    )
    trace["steps"].append({"agent": "knowledge_fusion", "context_length": len(fused_context)})

    # 7. Insight Agent
    answer = await insight_agent.generate_insight(fused_context)
    trace["steps"].append({"agent": "insight", "answer_length": len(answer)})
    trace["finished_at"] = str(datetime.utcnow())

    citation_sources = [
        {"filename": fname, "snippets": snips}
        for fname, snips in rag_result.get("snippets_by_source", {}).items()
    ]

    return {
        "content": answer,
        "charts": [chart_response] if chart_response else [],
        "files_used": plan["csv_file_ids"] + plan["doc_file_ids"],
        "citations": rag_result.get("citations", []),
        "citation_sources": citation_sources,
        "agent_trace": trace,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_csv_paths(datasets: list[dict], ids: list[str]) -> list[str]:
    id_set = set(ids)
    paths = []
    for d in datasets:
        if d["_id"] in id_set and d.get("cleaned_path"):
            paths.append(d["cleaned_path"])
    return paths


def _resolve_doc_meta(documents: list[dict], ids: list[str]) -> dict[str, str]:
    id_set = set(ids)
    return {
        d["_id"]: d["filename"]
        for d in documents
        if d["_id"] in id_set
    }
