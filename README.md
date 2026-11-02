# TDS Decision Support (India) — Student Prototype

A small experiment in using an LLM for **invoice-description classification** while keeping tax-rule decisions in deterministic, reviewable code.

> **Important:** This is an educational prototype, not tax advice or a production TDS calculator. The rule table in `data/rules.json` is explicitly a draft and has not been signed off by a Chartered Accountant. Do not use its amounts to deduct or deposit tax.

## Problem being explored

Accounts-payable teams receive vendor invoices with free-text descriptions such as “legal consultation”, “civil repair work”, “office rent” or “software licence plus implementation”. The description alone may not contain enough information to determine the correct withholding-tax treatment. A wrong classification can lead to an incorrect deduction or an avoidable compliance exception.

This prototype explores a narrow question:

**Can an LLM classify an invoice description into a controlled set of payment categories, quote the exact words supporting its classification, and then hand the result to a deterministic rules engine that either produces a provisional calculation or routes uncertainty to a human reviewer?**

The intended user is an accounts-payable analyst. The system is decision support only; a qualified tax professional remains accountable for the final treatment.

## Design choices

- `tds/classify.py`: a keyword baseline and an optional OpenRouter LLM classifier. The classifier returns only a category, a verbatim evidence snippet and a confidence value. It is not allowed to return a rate or tax amount.
- `tds/rules.py`: deterministic arithmetic using `Decimal` and a draft, effective-dated rule table.
- `tds/pipeline.py`: checks whether the evidence exists in the source description, applies a confidence gate and routes ambiguous cases to review.
- `data/cases.json`: 16 synthetic invoice descriptions and expected outcomes.
- `tests/test_rules.py`: unit tests for the rule engine and safety gates.
- `run_eval.py`: evaluates the simple keyword baseline or, when configured, an LLM classifier.

A deliberate safety change: purchase-of-goods cases are **not** treated as “0% TDS and approved”. The separate buyer-side goods-purchase provision is outside the prototype, so such cases are routed to review and no TDS amount is calculated.

## Current scope

Included:
- Resident-payee examples only.
- A limited set of contractor, professional, technical, rent and commission categories.
- Synthetic invoice text and structured ERP-like context (taxable value, payee type, PAN status, year-to-date paid).
- Confidence/evidence gates and human-review routing.
- A basic prompt-injection test case.

Not included:
- Non-resident payments and treaty analysis.
- Goods-purchase withholding applicability.
- TCS, salary TDS, GST treatment, credit notes, lower/nil deduction certificates, exemptions, multiple invoice lines, mixed supplies or complex contracts.
- End-to-end PDF/OCR extraction or ERP integration.
- Production audit logging, authentication, tenant isolation or deployment.
- A legally validated rate/threshold table.

## Setup

Python 3.9+; the core project uses the standard library.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
python run_eval.py
```

macOS/Linux:
```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
python run_eval.py
```

The evaluation writes `RESULTS_BASELINE.md`.

## Optional LLM evaluation

1. Create an API key with a model provider supported by OpenRouter.
2. Set environment variables in your terminal (do not commit keys):
   - Windows PowerShell: `$env:OPENROUTER_API_KEY="..."`
   - Windows PowerShell: `$env:OPENROUTER_MODEL="provider/model:free"`
   - macOS/Linux: `export OPENROUTER_API_KEY="..."`
   - macOS/Linux: `export OPENROUTER_MODEL="provider/model:free"`
3. Run:
```bash
python run_eval.py --llm
```
4. Record the exact model ID, date, test result and any failed cases in `RESULTS_LLM.md`.

The LLM evaluation has **not** been run as part of this repository snapshot unless an actual results file with model/date is present. Do not claim model accuracy before running it.

## Known risks and next steps

1. The rule table is a draft and must be checked against the applicable legislation, rules, notifications and a CA-reviewed interpretation before any rate is relied upon.
2. For TDS, the legally relevant event can be the earlier of credit or payment; this prototype currently uses a single `date` field. A proper version needs both dates and must derive the trigger date.
3. Applicability can depend on payer type, payee residency, payee category, PAN, aggregate payments, transaction nature and other statutory conditions. The current structured inputs are incomplete.
4. Threshold-crossing cases need a reviewed catch-up calculation and an auditable payment ledger; this prototype routes them to a human.
5. Category classification can be wrong even with a verbatim evidence snippet. For example, “rental of a conference hall” may not be equivalent to a lease of a building. The current baseline has a known unsafe classification in this area.
6. The 16 synthetic examples are a smoke test, not a statistically meaningful benchmark.

See [`docs/DECISIONS_AND_LIMITATIONS.md`](docs/DECISIONS_AND_LIMITATIONS.md) for the design review and official reference links.

## Data and privacy

All examples are invented. No PAN, GSTIN, bank details, vendor identity or real invoice data is included. Never upload confidential supplier or taxpayer records to a public repository or an external model API.

## What I would build next

- Replace the draft rule table with a CA-reviewed, source-linked and versioned rule catalogue.
- Add credit-date/payment-date handling and payer/payee applicability gates.
- Add a document-level evidence model with source page and bounding-box references.
- Expand the benchmark with ambiguous and adversarial cases reviewed by a tax practitioner.
- Add a reviewer interface and immutable decision/audit events.
