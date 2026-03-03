import argparse, re, yaml
from pathlib import Path

RULES = [
    ("SIM_TOOL_MISSING", re.compile(r"(XSIM not found|xvlog.*not found|xelab.*not found|xsim.*not found)", re.I)),
    ("COMPILE_ERROR", re.compile(r"(ERROR:|Syntax error|xvlog: ERROR|vlog-)", re.I)),
    ("ELAB_ERROR", re.compile(r"(xelab: ERROR|elaboration|Failed to elaborate)", re.I)),
    ("RUNTIME_ERROR", re.compile(r"(FATAL:|Segmentation fault|\$fatal|UVM_FATAL)", re.I)),
]

def classify(text: str) -> str:
    for label, pat in RULES:
        if pat.search(text):
            return label
    if "HELLO_TB_DONE" in text or "run all" in text:
        return "PASS_LIKELY"
    return "UNKNOWN"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", help="reports/run_<id>")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    logs_dir = run_dir / "logs"
    if not logs_dir.exists():
        raise SystemExit(f"Missing {logs_dir}")

    triage = []
    for log in sorted(logs_dir.glob("*.log")):
        txt = log.read_text(errors="ignore")
        triage.append({
            "test": log.stem,
            "classification": classify(txt),
            "log": str(log).replace("\\","/"),
        })

    out = run_dir / "triage.yaml"
    out.write_text(yaml.safe_dump({"triage": triage}, sort_keys=False))
    print(f"[ok] wrote {out}")

if __name__ == "__main__":
    main()