import os, subprocess, shutil
from pathlib import Path

def _run(cmd, cwd=None):
    print("[cmd]", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=True)

def run_xsim(top: str, sources: list[str], outdir: str, waves: bool=False):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    xvlog = shutil.which("xvlog")
    xelab = shutil.which("xelab")
    xsim  = shutil.which("xsim")
    if not (xvlog and xelab and xsim):
        raise RuntimeError("XSIM not found (need xvlog/xelab/xsim in PATH). Source your Vivado/cadtools script first.")

    # Compile
    _run([xvlog, "-sv", *sources], cwd=out)

    # Elaborate
    _run([xelab, top, "-snapshot", "work.sim"], cwd=out)

    # Run
    tcl = out / "run.tcl"
    if waves:
        # XSIM supports wdb; this is minimal and works for most cases
        tcl.write_text("log_wave -r /*\nrun all\nquit\n")
        _run([xsim, "work.sim", "-tclbatch", str(tcl)], cwd=out)
    else:
        tcl.write_text("run all\nquit\n")
        _run([xsim, "work.sim", "-tclbatch", str(tcl)], cwd=out)
