# GitHub upload steps (Windows / VS Code)

## 1. Extract the project
1. Download `tds-assistant-github-ready.zip`.
2. Right-click the ZIP -> Extract All.
3. Open the extracted `tds-assistant` folder in VS Code.

## 2. Run it before publishing
Open Terminal -> New Terminal and run:

```powershell
python -m unittest discover -s tests -v
python run_eval.py
```

Expected in this checked version:
- 12 unit tests pass.
- Keyword baseline: 15/16 cases fully correct.
- 0 dangerous auto-approval misses in this small synthetic set.
- 1 false alarm (a case sent to review unnecessarily).

This is a 16-case synthetic smoke test, not a real-world accuracy claim. The optional LLM evaluation has not been run.

## 3. Create a GitHub repository
1. Sign in to https://github.com
2. Click the `+` icon -> New repository.
3. Repository name: `tds-decision-support`
4. Description: `A student prototype for evidence-backed TDS classification and human-reviewed compliance decisions.`
5. Choose Public if the assessment requires a publicly accessible link.
6. Do not initialize with a README (the project already has one).
7. Click Create repository.

## 4. Push using Git
In the VS Code terminal, make sure you are inside the project folder:

```powershell
git init
git add .
git status
git commit -m "Initial prototype: TDS classification and rules engine"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/tds-decision-support.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub may ask you to sign in through the browser.

If Git says `remote origin already exists`, use:
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/tds-decision-support.git
```

## 5. Make the repository feel like a real engineering project
Do not fake a commit history or claim work you did not do. Make a few genuine improvements after you understand each part, and commit each one separately. For example:

```powershell
git add README.md docs/
git commit -m "Document scope, architecture and known limitations"

git add tds/ tests/
git commit -m "Route out-of-scope and ambiguous cases to review"

git add RESULTS_BASELINE.md
git commit -m "Record keyword baseline evaluation"
```

Only use these example commits if you actually made and reviewed those changes. Do not backdate commits.

## 6. Add a short GitHub repository description
Suggested description:
`Student prototype: LLM-assisted invoice-description classification with deterministic TDS rules, evidence checks and human-review routing.`

Suggested topics:
`python`, `llm`, `openrouter`, `tax-compliance`, `decision-support`, `human-in-the-loop`, `rule-engine`

## 7. Final checks before sharing
- Open the repository in a private/incognito browser window to confirm it is public.
- Confirm `README.md`, `data/`, `tds/`, `tests/`, `docs/` and `RESULTS_BASELINE.md` are visible.
- Confirm there is no `.env`, API key, PAN, GSTIN, vendor data or private information.
- Share the repository URL in the assessment form.
- Include your actual LLM conversation logs separately if requested by Tresata.

## Optional LLM run
Do this only if you have time. Set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` in your terminal, then run:

```powershell
python run_eval.py --llm
```

Record the exact model ID, date, and full results. Do not write that an LLM run passed unless you actually ran it. Keep API keys out of GitHub.
