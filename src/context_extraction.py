"""Aspect-aware context extraction used in the Taaghche ABSA project.

The logic mirrors the rules used in the research notebook. It loads frozen
regular-expression patterns from config/taaghche_frozen_aspect_rules.json,
finds aspect anchors, merges adjacent anchors of the same aspect, and returns
aspect-specific text spans.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_PATH = ROOT / "config" / "taaghche_frozen_aspect_rules.json"
BOUNDARY_WORDS = ["ولی", "اما", "با این حال"]


def load_patterns(rules_path: Path = DEFAULT_RULES_PATH):
    with open(rules_path, "r", encoding="utf-8") as f:
        frozen_rules = json.load(f)

    aspect_patterns = {
        aspect: re.compile(pattern)
        for aspect, pattern in frozen_rules["aspect_patterns"].items()
    }
    author_pattern = re.compile(frozen_rules["author_generic_pattern"])
    return aspect_patterns, author_pattern


def extract_aspect_anchors(text: str, aspect_patterns, author_pattern) -> List[Dict]:
    anchors = []

    for aspect, pattern in aspect_patterns.items():
        for match in pattern.finditer(text):
            anchors.append(
                {
                    "aspect": aspect,
                    "anchor": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    for match in author_pattern.finditer(text):
        anchors.append(
            {
                "aspect": "author",
                "anchor": match.group(),
                "start": match.start(),
                "end": match.end(),
            }
        )

    return anchors


def merge_same_aspect_anchors(anchors: List[Dict]) -> List[Dict]:
    if not anchors:
        return []

    anchors = sorted(anchors, key=lambda x: x["start"])
    merged = []
    current = anchors[0].copy()

    for anchor in anchors[1:]:
        if anchor["aspect"] == current["aspect"]:
            current["end"] = anchor["end"]
        else:
            merged.append(current)
            current = anchor.copy()

    merged.append(current)
    return merged


def clean_context_boundary(context: str) -> str:
    context = context.strip()
    for word in BOUNDARY_WORDS:
        if context.endswith(word):
            context = context[: -len(word)].strip()
    return context


def extract_aspect_contexts(text: str, aspect_patterns, author_pattern) -> List[Dict[str, str]]:
    anchors = merge_same_aspect_anchors(
        extract_aspect_anchors(text, aspect_patterns, author_pattern)
    )

    if not anchors:
        return []

    contexts = []
    for i, anchor in enumerate(anchors):
        start = 0 if i == 0 else anchor["start"]
        end = anchors[i + 1]["start"] if i < len(anchors) - 1 else len(text)
        context = clean_context_boundary(text[start:end])
        contexts.append({"aspect": anchor["aspect"], "context": context})

    return contexts


if __name__ == "__main__":
    patterns, author_pattern = load_patterns()
    examples = [
        "ترجمه خوب بود داستان عالی بود",
        "نویسنده عالی بود ولی داستان ضعیف بود",
    ]

    for text in examples:
        print(f"\nTEXT: {text}")
        for item in extract_aspect_contexts(text, patterns, author_pattern):
            print(f"- {item['aspect']}: {item['context']}")
