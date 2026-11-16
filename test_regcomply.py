"""Exercise the evidence API with synthetic rules and identifiers."""

from regcomply import Passage, ask, diff_versions, review


def corpus() -> list[Passage]:
    # Synthetic revisions make the intended diff unambiguous.
    return [
        {
            "id": "demo-v1",
            "rule": "demo",
            "version": "v1",
            "url": "https://example.invalid",
            "text": "Retain records.\n",
            "terms": ["records"],
        },
        {
            "id": "demo-v2",
            "rule": "demo",
            "version": "v2",
            "url": "https://example.invalid",
            "text": "Retain records for review.\n",
            "terms": ["records"],
        },
    ]


def test_REQ_01_cited_retrieval() -> None:
    assert ask("Which records?", corpus())["evidence"] == corpus()


def test_REQ_02_out_of_scope() -> None:
    assert ask("How tall is a mountain?", corpus())["status"] == "insufficient_evidence"


def test_REQ_03_redaction_before_review() -> None:
    matches = review("Records for analyst@example.invalid 123-45-6789 account #12345678", corpus())
    assert matches[0]["passage"] == "Records for [EMAIL] [SSN] account #[ACCOUNT]"


def test_REQ_04_version_diff() -> None:
    assert "+Retain records for review." in diff_versions("demo", "v1", "v2", corpus())
