"""Deterministic TDS decision engine. No LLM here. All money in Decimal."""
import json, pathlib
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

RULES = json.loads((pathlib.Path(__file__).parent.parent / "data" / "rules.json").read_text())

def _d(x): return Decimal(str(x))

def decide(category, payee_type, pan_valid, ytd_before, taxable_value, pay_date, rules=RULES):
    cats = rules["categories"]
    out = {"category": category, "rate": None, "tds": Decimal(0), "label": None,
           "regime": None, "applicable": False, "flags": []}
    if category not in cats:
        out["flags"].append("unknown_category"); return out
    c = cats[category]
    regime_2025 = date.fromisoformat(pay_date) >= date.fromisoformat(rules["cutover"])
    out["regime"] = "ITA-2025" if regime_2025 else "ITA-1961"
    out["label"] = c.get("label_2025") if regime_2025 else c.get("label_1961")
    if c.get("ambiguous"):
        out["flags"].append("ambiguous_category"); return out
    if c.get("no_tds"):
        # This prototype does not implement buyer-side TDS on goods (e.g. the
        # separate purchase-of-goods provision). Do not silently return 0%.
        out["tds"] = None
        out["flags"].append("goods_purchase_rule_out_of_scope: requires separate applicability checks")
        return out
    amt, ytd = _d(taxable_value), _d(ytd_before)
    single, agg = c.get("single_threshold"), c.get("agg_threshold")
    by_single = single is not None and amt > single
    by_agg = agg is not None and ytd + amt > agg
    applicable = True if (single is None and agg is None) else (by_single or by_agg)
    if applicable and by_agg and not by_single and 0 < ytd <= agg:
        out["flags"].append("threshold_crossed_on_this_invoice: earlier payments may need TDS too; CA to confirm")
    if not applicable:
        return out
    rate = _d(c["rate"][payee_type])
    if not pan_valid:
        rate = max(rate * 2, _d(rules["no_pan_rate"]))
        out["flags"].append("no_valid_PAN_higher_rate")
    out.update(applicable=True, rate=rate,
               tds=(amt * rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return out
