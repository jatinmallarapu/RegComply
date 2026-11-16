"""Find and review cited regulatory evidence without a remote model."""

import argparse
import difflib
import json
import re
from pathlib import Path
from typing import TypedDict

# Ignore common question words so they do not turn unrelated rules into evidence.
STOP = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "does",
    "for",
    "is",
    "must",
    "of",
    "the",
    "to",
    "what",
    "when",
}
IDENTIFIERS = (
    (r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "[EMAIL]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
    (r"(?i)(\baccount(?:\s+(?:number|no\.?))?\s*[:#]?\s*)\d{6,20}\b", r"\1[ACCOUNT]"),
)


class Passage(TypedDict):
    id: str
    rule: str
    version: str
    url: str
    text: str
    terms: list[str]


def redact(text: str) -> str:
    for pattern, replacement in IDENTIFIERS:
        text = re.sub(pattern, replacement, text)
    return text


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold())) - STOP


def search(question: str, corpus: list[Passage], limit: int = 3) -> list[Passage]:
    query = tokens(redact(question))
    relevant = [(len(query & set(row["terms"])), row) for row in corpus]
    return [
        row for count, row in sorted(relevant, key=lambda item: (-item[0], item[1]["id"])) if count
    ][:limit]


def ask(question: str, corpus: list[Passage]) -> dict[str, object]:
    matches = search(question, corpus)
    return {"status": "evidence_found" if matches else "insufficient_evidence", "evidence": matches}


def review(text: str, corpus: list[Passage]) -> list[dict[str, object]]:
    # Redact before splitting so addresses remain intact long enough to mask.
    return [
        {"passage": passage, "evidence": evidence}
        for passage in re.split(r"(?<=[.!?])\s+|\n+", redact(text))
        if (evidence := search(passage, corpus))
    ]


def diff_versions(rule: str, before: str, after: str, corpus: list[Passage]) -> str:
    versions = {p["version"]: p["text"] for p in corpus if p["rule"] == rule}
    return "".join(
        difflib.unified_diff(
            versions[before].splitlines(keepends=True),
            versions[after].splitlines(keepends=True),
            fromfile=before,
            tofile=after,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["ask", "review"])
    parser.add_argument("input", help="Question text or path to a plain-text document")
    parser.add_argument("--corpus", type=Path, default=Path("examples/corpus.json"))
    args = parser.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    result = (
        ask(args.input, corpus)
        if args.mode == "ask"
        else review(Path(args.input).read_text(encoding="utf-8"), corpus)
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
