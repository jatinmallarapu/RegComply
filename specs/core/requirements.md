# Cited regulatory research

A compliance analyst needs to locate a relevant rule and inspect the source passage before drafting a review memo.

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| REQ-01 | Source-backed retrieval | GIVEN a question with overlapping terms WHEN searched THEN matching source passages appear with their citation IDs. |
| REQ-02 | Out-of-scope requests | GIVEN a question with no matching terms WHEN searched THEN return an explicit insufficient-evidence status. |
| REQ-03 | Sensitive document review | GIVEN an email, labeled account number or SSN WHEN reviewed THEN mask it before matching rules. |
| REQ-04 | Rule version history | GIVEN two explicit versions of a rule WHEN compared THEN return a unified diff. |
