"""L5 bridge to the external legal-RAG project (default C:/Users/gauri/Projects/rag).

That project is a LangGraph RAG (hybrid dense bge-m3 + BM25 + RRF + cross-encoder
rerank; Ollama/Claude answers with inline citations and IN FORCE / PROPOSED / DRAFT /
REVOKED status) over 15 real policy PDFs. We integrate its **frozen, human-verified
corpus manifest** (`sources.csv`) as the citation/evidence base for the four-axis gap
matrix. The retrieval + LLM steps run in the RAG's own venv (they need Ollama or an
API key) and are NOT invoked by the pipeline — `answer_live()` is an optional hook.

The manifest is copied into `config/policy_sources.csv` so dcfootprint stays
self-contained and reproducible; point `DCF_RAG_DIR` at the live project to refresh it.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pandas as pd

from dcfootprint.io.facilities import _repo_root

RAG_DIR = Path(os.environ.get("DCF_RAG_DIR", r"C:/Users/gauri/Projects/rag"))

# RAG corpus topic -> the four-axis the instrument is NEAREST to. None of the docs
# actually mandate our four axes (that is the gap); this only labels the closest ones.
_TOPIC_AXIS = {
    "carbon_intensity": "carbon_intensity",
    "electricity_consumption": "carbon_intensity",     # PUE / rate / grid-connection
    "water_stress": "scarcity_weighted_water",
    "water_storage": "scarcity_weighted_water",
    "temperature": None,                                # cooling — no axis
    "datacenter_mapping": None,
    "siting_general": "scarcity_weighted_water",
}


def load_manifest() -> pd.DataFrame:
    """The cited, status-flagged policy corpus (local copy first, else the live RAG)."""
    local = _repo_root() / "dcfootprint" / "config" / "policy_sources.csv"
    path = local if local.exists() else RAG_DIR / "sources.csv"
    df = pd.read_csv(path)
    df["in_force"] = df["status"].astype(str).str.upper().str.startswith("IN FORCE")
    df["axis_nearest"] = df["topic"].map(_TOPIC_AXIS)
    return df


def cited_constraints() -> pd.DataFrame:
    """In-force instruments that actually bite (siting / efficiency / water), cited."""
    df = load_manifest()
    keep = df[df["in_force"]].copy()
    return keep[["jurisdiction", "title", "doc_type", "topic", "status", "url"]].reset_index(drop=True)


def corpus_summary() -> dict:
    df = load_manifest()
    return {
        "n_documents": int(len(df)),
        "n_in_force": int(df["in_force"].sum()),
        "n_proposed_or_draft": int((~df["in_force"]).sum()),
        "jurisdictions": sorted(df["jurisdiction"].unique().tolist()),
        "topics": sorted(df["topic"].unique().tolist()),
        "axes_directly_mandated": 0,     # corpus is the regulated *perimeter* — confirms the 4-axis gap
        "source": "external legal-RAG corpus (sources.csv), human-verified + status-flagged",
    }


def answer_live(question: str, timeout: int = 300) -> str | None:
    """OPTIONAL: run the external RAG in its own venv to (re)generate a cited answer.
    Needs Ollama running or ANTHROPIC_API_KEY. Not called by the pipeline; returns
    None if the venv/entrypoint isn't available."""
    py = RAG_DIR / "venv" / "Scripts" / "python.exe"
    if not (py.exists() and (RAG_DIR / "ask.py").exists()):
        return None
    try:
        r = subprocess.run([str(py), "ask.py", question], cwd=str(RAG_DIR),
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() or None
    except Exception:
        return None


if __name__ == "__main__":
    print("corpus:", corpus_summary())
    print("\nin-force cited constraints:")
    print(cited_constraints().to_string(index=False))
