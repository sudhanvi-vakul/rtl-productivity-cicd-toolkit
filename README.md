@'
# C0 — RTL Productivity + CI/CD Toolkit

Goal: one-command compile/run/regress with reproducible artifacts (logs/waves/report).

## Quickstart (XSIM)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

python scripts/run.py --tool xsim --suite smoke --test hello
python scripts/run.py --tool xsim --suite smoke --test hello --waves