# Design review: decisions, gaps and validation plan

## Why this is an AI + rules problem

The LLM is used for a narrow language task: map a free-text invoice description to one category from a closed list and quote a verbatim evidence substring. The LLM does not choose the statutory rate, calculate TDS, or approve a payment.

The rules engine performs numeric calculations using `Decimal`, effective dates and structured context. If classification evidence is absent, confidence is low, or a category is ambiguous, the pipeline routes the case to a human reviewer.

This split is intentional: natural-language interpretation is probabilistic; arithmetic and policy application should be deterministic and traceable.

## What the uploaded first version revealed

- The keyword baseline reported 14/16 fully correct cases.
- It made one unsafe auto-routing decision: “Rental of conference hall for annual event” was classified as `rent_building` and auto-routed even though the expected outcome was review.
- It made one unnecessary review: “Counsel charges for litigation support” was classified as unknown by the keyword baseline.
- The LLM path is optional and must be run separately; baseline results are not LLM results.

After review, goods-purchase cases were changed to route to human review because the separate buyer-side goods-purchase withholding provision is not implemented. A `0` amount must not be interpreted as a legal conclusion that no TDS applies.

## Material gaps before any real use

1. **Trigger date:** The code currently consumes one `date` field. The Income Tax Department says the applicable Act depends on the earlier of the credit or payment event. The data model should contain `credit_date` and `payment_date`, and derive the earlier applicable date.
2. **Incomplete applicability context:** The prototype does not comprehensively represent payer status/type, resident/non-resident status, payee status, transaction-specific exceptions, certificates, or all relevant statutory conditions.
3. **Unverified rules:** `data/rules.json` remains a draft. Rates, thresholds, table serial numbers and labels must be checked against the current Act, Rules, Finance Act changes and official guidance, and reviewed by a CA.
4. **Threshold-crossing logic:** The system flags some crossing cases but does not calculate any catch-up deduction on earlier credits/payments. It must not be used to calculate actual withholding.
5. **Ambiguous classification:** A text snippet alone may not distinguish a lease from a venue-hire service, or a software licence from implementation services. The correct action is to request contract/context and send the case to review.
6. **Benchmark size:** Sixteen synthetic cases are useful for smoke testing only. They cannot establish production accuracy or business value.

## Human-review principle

The prototype is decision support. A reviewer must see the original description, extracted evidence, structured inputs, rule version, flags and calculation explanation. No payment release or tax filing action should be automated.

## Official reference points consulted

- Income Tax Department, TDS Compliance FAQs: https://www.incometax.gov.in/iec/foportal/help/all-topics/e-filing-services/tds-compliance
  - Explains the 1 April 2026 transition and that the earlier of credit or payment determines which Act applies.
  - Explains that the new Act uses Section 393 for non-salary TDS and that old section references may cause reporting errors after the transition.
- Income-tax Act, 2025, Section 393: https://www.incometaxindia.gov.in/w/section-393-5
  - Statutory section to consult for resident-payee TDS categories; this repository does not reproduce or claim to fully implement it.
- Tresata public company profile: https://in.linkedin.com/company/tresata
  - Describes Tresata in terms of data-centric AI, inference and data accuracy systems. This supports a general technology fit, not a claim that Tresata offers TDS software or has requested this use case.

## Validation plan

- Have a CA validate each rule row and boundary condition.
- Add boundary tests at threshold-minus-one, threshold, threshold-plus-one.
- Add dates where credit and payment straddle 31 March / 1 April 2026.
- Add a test for resident vs non-resident and payer type.
- Test venue hire, software/SaaS, bundled services, goods plus installation and ambiguous contracts.
- Run the LLM evaluation with a named model, preserve raw model outputs, report per-class precision/recall and dangerous false-auto rate.
