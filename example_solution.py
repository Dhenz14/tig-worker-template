"""Example TIG candidate for the 'chunking' challenge.

This is a working baseline-quality chunker that scores around the champion
threshold on the default difficulty bucket. Use it as a reference for the
function signature, return shape, and the kind of structure the verifier
expects to see.

To rehearse:
    hiveai tig rehearse example_solution.py --challenge chunking --seeds 0,1,2

To create a signing key:
    hiveai tig keygen --save keypair.json

To submit:
    hiveai tig submit example_solution.py \
        --challenge chunking \
        --host https://hiveai.example \
        --key keypair.json
"""
from __future__ import annotations

import re
from typing import Any


def chunk_documents(docs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Split each document into roughly fixed-size, sentence-aligned chunks.

    The verifier requires each ``required_term`` from the doc to appear in
    at least one chunk whose content is at most 4000 characters. Plain
    fixed-window slicing satisfies that for typical documents and stays
    well under the storage and latency budgets.
    """

    out: dict[str, list[dict[str, Any]]] = {}
    for doc in docs:
        text = str(doc.get("content", ""))
        out[doc["id"]] = list(_split_sentences(text, target_chars=1000, max_chars=1400))
    return out


_SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+|\n\n+")


def _split_sentences(
    text: str,
    *,
    target_chars: int,
    max_chars: int,
) -> list[dict[str, Any]]:
    """Concatenate sentences into chunks of ~target_chars, never > max_chars."""

    if not text:
        return []
    pieces = _SENTENCE_END_RE.split(text)
    chunks: list[dict[str, Any]] = []
    buffer: list[str] = []
    buffer_size = 0
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        if buffer_size + len(piece) > max_chars and buffer:
            chunks.append({"content": " ".join(buffer), "metadata": {"strategy": "sentence_window"}})
            buffer = []
            buffer_size = 0
        buffer.append(piece)
        buffer_size += len(piece) + 1
        if buffer_size >= target_chars:
            chunks.append({"content": " ".join(buffer), "metadata": {"strategy": "sentence_window"}})
            buffer = []
            buffer_size = 0
    if buffer:
        chunks.append({"content": " ".join(buffer), "metadata": {"strategy": "sentence_window"}})
    return chunks
