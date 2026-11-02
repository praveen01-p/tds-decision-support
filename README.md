# TDS Decision Support (India) — Student Prototype

A small experiment in using an LLM for **invoice-description classification** while keeping tax-rule decisions in deterministic, reviewable code.

> **Important:** This is an educational prototype, not tax advice or a production TDS calculator. The rule table in `data/rules.json` is a draft and has not been signed off by a Chartered Accountant (CA). Do not use its amounts to deduct or deposit tax.

## Problem being explored

Accounts-payable teams receive vendor invoices with free-text descriptions such as “legal consultation”, “civil repair work”, “office rent” or “software licence plus implementation”. The description alone may not contain enough information to determine the correct withholding-tax treatment. A wrong classification can lead to an incorrect deduction or an avoidable compliance exception.

This prototype explores a narrow question:

**Can an LLM classify an invoice description into a controlled set of payment categories, quote the exact words supporting its classification, and then hand the result to a deterministic rules engine that either produces a provisional calculation or routes uncertainty to a human reviewer?**

The intended user is an accounts-payable analyst. The system is decision support only; a qualified tax professional remains accountable for the final treatment.

## How the prototype works

1. **Invoice description and structured context:** The pipeline receives the description and limited structured fields, such as taxable value, payee type, PAN status, year-to-date payments and a transaction date.
2. **Classification:** `tds/classify.py` uses a keyword baseline or an optional OpenRouter LLM classifier. The classifier returns a category, a verbatim evidence snippet and a confidence value. It must not return a tax rate or amount.
3. **Validation and routing:** `tds/pipeline.py` checks that the category is in the controlled catalogue, verifies that the evidence appears in the original description, applies a confidence threshold of `0.8`, and adds ambiguity flags. Blocking flags route the case to human review.
4. **Deterministic calculation:** `tds/rules.py` applies the draft rule table using `Decimal` arithmetic and effective-date labels. It does not rely on the LLM for arithmetic.
5. **Human decision:** The prototype provides decision support only. It does not automate payment release or tax filing.

A deliberate safety choice: purchase-of-goods cases are **not** treated as “0% TDS and approved”. The separate buyer-side goods-purchase withholding provision is outside this prototype, so such cases are routed to review and no TDS amount is calculated.

## Project structure

- `tds/classify.py` — keyword baseline and optional OpenRouter LLM classifier.
- `tds/rules.py` — deterministic rule application and arithmetic using `Decimal`.
- `tds/pipeline.py` — evidence checks, confidence gate, ambiguity flags and human-review routing.
- `data/rules.json` — draft, effective-dated rule table; not legally validated.
- `data/cases.json` — 16 synthetic invoice descriptions and expected outcomes.
- `tests/test_rules.py` — unit tests for the rule engine and safety gates.
- `run_eval.py` — runs the keyword-baseline evaluation or, when configured, the optional LLM evaluation.
- `docs/DECISIONS_AND_LIMITATIONS.md` — design decisions, limitations and validation plan.
- `RESULTS_BASELINE.md` — recorded keyword-baseline evaluation output.

## Current scope

Included:
- Synthetic resident-payee examples only.
- A limited set of contractor, professional, technical, rent and commission categories, plus goods-purchase and ambiguous categories that are routed for review.
- Synthetic invoice text and structured ERP-like context (taxable value, payee type, PAN status and year-to-date paid amount).
- Evidence and confidence gates, ambiguity flags and human-review routing.
- A basic prompt-injection test case.

Not included:
- Non-resident payments and treaty analysis.
- Complete goods-purchase withholding applicability checks.
- TCS, salary TDS, GST treatment, credit notes, lower/nil deduction certificates or exemptions.
- Multiple invoice lines, mixed supplies or complex contract interpretation.
- End-to-end PDF/OCR extraction or ERP integration.
- Production audit logging, authentication, tenant isolation or deployment.
- A legally validated rate/threshold table.

## Setup

Python 3.9+; the core project uses the standard library.

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
python run_eval.py
```

### macOS/Linux

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
python run_eval.py
```

The evaluation writes or updates `RESULTS_BASELINE.md`.

## Baseline evaluation

The repository snapshot contains a **keyword-baseline** evaluation over 16 synthetic cases. The recorded evaluator output reports:

- Evaluator-reported pass count: **15/16**.
- Dangerous misses (auto-approved when review was expected): **0**.
- False alarms (sent to review when auto-routing was expected): **1**.
- Auto-approved cases with an incorrect TDS amount: **0**.

**Interpretation caveat:** 15/16 is the evaluator's reported score, not a real-world accuracy estimate or a representative benchmark. The evaluator treats an expected category of `unknown` as category-correct when routing and amount checks pass, even if the predicted category differs. For example, C15 predicts `rent_building` for conference-hall hire but is routed to review by a specific venue-hire ambiguity flag; C16 predicts `contractor_work` for a mixed goods-and-work description but is routed to review because confidence is low. C14 is the recorded false alarm: the keyword baseline does not recognise “Counsel charges for litigation support” and sends it to review. The 16 cases are synthetic smoke tests only.

The optional LLM evaluation has **not** been run in this repository snapshot. No LLM accuracy result is claimed.

## Optional LLM evaluation

1. Create an API key with a model provider supported by OpenRouter.
2. Set the environment variables in your terminal. Do not commit API keys.

   Windows PowerShell:

   ```powershell
   $env:OPENROUTER_API_KEY="YOUR_API_KEY"
   $env:OPENROUT
