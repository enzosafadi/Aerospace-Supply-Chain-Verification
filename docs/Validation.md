# Aerospace - Validation Record

Review date: 27 October 2026.

## Automated checks

Command: `python -m unittest -v test_app.py`

| Scenario | Result | What it establishes |
|---|---|---|
| Create an order | PASS | Stored total and initial event chain are consistent |
| Complete workflow | PASS | Creation through verification produces four events |
| Invalid transition | PASS | Delivery from Created is rejected |
| Change an event actor | PASS | Recalculation detects the modified event |

## Scope of evidence

These four tests do not establish production security, performance, regulatory compliance, concurrent-user correctness or resistance to a database administrator rewriting the entire history. No business outcome has been measured.

The startup default was corrected from port 10000 to 8000 so the quick start matches the running application. A supplied PORT environment variable still overrides the default.

## HTTP walkthrough

A temporary local HTTP server returned the three seed orders and CA$25,478.50 total value. Requests advanced order 1 through approval, delivery and verification; order 2 was approved. The metrics returned one verified order and the audit endpoint returned `{"valid": true, "events": 4}`.

## Screenshot coverage

Application screenshots are not included in this release. The optional `tools/Capture-Screenshots.cjs` script captures the demonstration when Playwright and Chromium are installed locally. Automated test results above do not establish browser visual coverage.
