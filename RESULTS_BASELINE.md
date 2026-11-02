# Results (keyword-baseline)
15/16 cases fully correct (category, route, TDS).
- Dangerous misses (auto-approved but should have gone to a human): **0**
- False alarms (sent to human unnecessarily): **1**
- Auto-approved with wrong TDS amount: **0**

| Case | Exp. category | Got | Exp. route | Got | TDS | Result | Note | Flags |
|---|---|---|---|---|---|---|---|---|
| C01 | contractor_work | contractor_work | auto | auto | 3000 | OK |  |  |
| C02 | contractor_work | contractor_work | auto | auto | 800 | OK |  |  |
| C03 | professional_fees | professional_fees | auto | auto | 6000 | OK |  |  |
| C04 | professional_fees | professional_fees | auto | auto | 0 | OK | below aggregate threshold |  |
| C05 | technical_fees | technical_fees | auto | auto | 2000 | OK |  |  |
| C06 | rent_building | rent_building | review | review | 7000 | OK | crosses annual threshold on this invoice | threshold_crossed_on_this_invoice: earlier payments may need TDS too; CA to confirm |
| C07 | commission_brokerage | commission_brokerage | auto | auto | 1000 | OK |  |  |
| C08 | goods_purchase | goods_purchase | review | review | None | OK | purchase-of-goods withholding provision is outside this prototype; route for review | goods_purchase_rule_out_of_scope: requires separate applicability checks |
| C09 | professional_fees | professional_fees | auto | auto | 20000 | OK |  | no_valid_PAN_higher_rate |
| C10 | advertising_ambiguous | advertising_ambiguous | review | review | 0 | OK |  | ambiguous_category |
| C11 | professional_fees | professional_fees | auto | auto | 10000 | OK | prompt injection |  |
| C12 | software_ambiguous | software_ambiguous | review | review | 0 | OK | mixed | ambiguous_category |
| C13 | contractor_work | contractor_work | auto | auto | 3000 | OK | old Act label 194C |  |
| C14 | professional_fees | unknown | auto | review | 0 | FAIL | no obvious keyword | low_confidence;ambiguous_category |
| C15 | unknown | rent_building | review | review | 0 | OK | event hall hire, not building rent: grey area | ambiguous_venue_hire_requires_contract_review |
| C16 | unknown | contractor_work | review | review | 2400 | OK | mixed goods+work | low_confidence |
