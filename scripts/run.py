import argparse, yaml, time
from pathlib import Path
from scripts.adapters.xsim import run_xsim

def load_tests(path="tests.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", default="xsim", choices=["xsim"])
    ap.add_argument("--test", default="hello")
    ap.add_argument("--suite", default="smoke")
    ap.add_argument("--waves", action="store_true")
    args = ap.parse_args()

    cfg = load_tests("tests.yaml")
    tests = cfg.get(args.suite, [])
    t = next((x for x in tests if x["name"] == args.test), None)
    if not t:
        raise SystemExit(f"Test '{args.test}' not found in suite '{args.suite}'")

    run_id = time.strftime("run_%Y%m%d_%H%M%S")
    outdir = Path("reports") / run_id
    outdir.mkdir(parents=True, exist_ok=True)

    sources = t["rtl"] + t["tb"]
    top = t["top"]

    if args.tool == "xsim":
        run_xsim(top=top, sources=sources, outdir=str(outdir), waves=args.waves)

    print(f"[ok] reports saved to {outdir}")

if __name__ == "__main__":
    main()
