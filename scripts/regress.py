import argparse, time, yaml, subprocess, sys
from pathlib import Path

def _run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", default="xsim", choices=["xsim"])
    ap.add_argument("--suite", default="smoke")
    ap.add_argument("--waves", action="store_true")
    args = ap.parse_args()

    with open("tests.yaml","r") as f:
        cfg = yaml.safe_load(f) or {}

    tests = cfg.get(args.suite, [])
    if not tests:
        raise SystemExit(f"No tests found for suite '{args.suite}'")

    run_id = time.strftime("run_%Y%m%d_%H%M%S")
    outroot = Path("reports") / run_id
    (outroot / "logs").mkdir(parents=True, exist_ok=True)

    results = []

    for t in tests:
        name = t["name"]
        log = outroot / "logs" / f"{name}.log"
        cmd = [sys.executable, "scripts/run.py", "--tool", args.tool, "--suite", args.suite, "--test", name]
        if args.waves:
            cmd.append("--waves")

        r = _run(cmd)
        log.write_text((r.stdout or "") + "\n" + (r.stderr or ""))

        results.append({
            "name": name,
            "rc": r.returncode,
            "log": str(log).replace("\\","/"),
        })

    (outroot / "results.yaml").write_text(yaml.safe_dump({"run_id": run_id, "suite": args.suite, "tool": args.tool, "results": results}, sort_keys=False))
    print(f"[ok] regress finished: {outroot}")

if __name__ == "__main__":
    main()