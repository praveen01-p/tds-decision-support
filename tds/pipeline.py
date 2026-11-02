from .rules import decide, RULES
from .classify import CATALOG

def process(case, classifier):
    cls = classifier(case["text"])
    flags = []
    # Venue/event-space hire can be a different legal/commercial arrangement
    # from a lease of land/building. The short description is insufficient.
    ambiguous_context_terms = ("conference hall", "event hall", "banquet hall", "venue hire")
    if any(term in case["text"].lower() for term in ambiguous_context_terms):
        flags.append("ambiguous_venue_hire_requires_contract_review")
    cat = cls.get("category")
    if cat not in CATALOG: flags.append("invalid_category"); cat = "unknown"
    ev = (cls.get("evidence") or "").lower()
    if cat != "unknown" and (not ev or ev not in case["text"].lower()):
        flags.append("evidence_not_found_in_invoice")
    try: conf = float(cls.get("confidence", 0))
    except Exception: conf = 0.0
    if conf < 0.8: flags.append("low_confidence")
    d = decide(cat, case["payee_type"], case["pan_valid"], case["ytd_paid"], case["taxable_value"], case["date"])
    flags += d["flags"]
    blocking = [f for f in flags if f != "no_valid_PAN_higher_rate"]
    return {"id": case["id"], "category": cat,
            "tds": None if d["tds"] is None else int(d["tds"]), "label": d["label"],
            "regime": d["regime"], "route": "review" if blocking else "auto", "flags": flags,
            "rule_version": RULES["version"]}
