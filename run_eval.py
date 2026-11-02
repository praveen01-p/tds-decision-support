"""python run_eval.py            -> keyword baseline (offline)
   python run_eval.py --llm      -> LLM classifier (needs OPENROUTER_API_KEY, OPENROUTER_MODEL)"""
import json, sys, time
from tds import classify
from tds.pipeline import process
use_llm = "--llm" in sys.argv
clf = classify.llm if use_llm else classify.baseline
name = "LLM:" + __import__("os").environ.get("OPENROUTER_MODEL", "?") if use_llm else "keyword-baseline"
cases = json.load(open("data/cases.json"))
rows, dangerous, false_alarm, wrong_tds = [], 0, 0, 0
for c in cases:
    r = process(c, clf); time.sleep(1 if use_llm else 0)
    cat_ok = r["category"] == c["exp_category"]
    route_ok = r["route"] == c["exp_route"]
    tds_ok = c["exp_tds"] is None or r["tds"] == c["exp_tds"] or r["route"] == "review"
    if r["route"] == "auto" and c["exp_route"] == "review": dangerous += 1
    if r["route"] == "review" and c["exp_route"] == "auto": false_alarm += 1
    if r["route"] == "auto" and c["exp_tds"] is not None and r["tds"] != c["exp_tds"]: wrong_tds += 1
    rows.append((c["id"], c["exp_category"], r["category"], c["exp_route"], r["route"], r["tds"], "OK" if (cat_ok or c["exp_category"] == "unknown") and route_ok and tds_ok else "FAIL", c["note"], ";".join(r["flags"])))
passed = sum(x[6] == "OK" for x in rows)
md = [f"# Results ({name})", f"{passed}/{len(rows)} cases fully correct (category, route, TDS).",
      f"- Dangerous misses (auto-approved but should have gone to a human): **{dangerous}**",
      f"- False alarms (sent to human unnecessarily): **{false_alarm}**",
      f"- Auto-approved with wrong TDS amount: **{wrong_tds}**", "",
      "| Case | Exp. category | Got | Exp. route | Got | TDS | Result | Note | Flags |", "|---|---|---|---|---|---|---|---|---|"]
md += ["| " + " | ".join(map(str, r)) + " |" for r in rows]
open("RESULTS_LLM.md" if use_llm else "RESULTS_BASELINE.md", "w").write("\n".join(md) + "\n")
print("\n".join(md))
