import subprocess
import shutil
from pathlib import Path
from typing import List, Optional


def _run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    print("[cmd]", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def run_xsim(top: str, sources: List[str], outdir: str, waves: bool = False) -> None:
    # Make output dir absolute to avoid any double-relative path bugs
    out = Path(outdir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Repo root = .../rtl-productivity-cicd-toolkit
    repo = Path(__file__).resolve().parents[2]

    # Make sources absolute so running from out/ never breaks paths
    abs_sources = [str((repo / s).resolve()) for s in sources]

    xvlog = shutil.which("xvlog")
    xelab = shutil.which("xelab")
    xsim = shutil.which("xsim")
    if not (xvlog and xelab and xsim):
        raise RuntimeError(
            "XSIM not found (need xvlog/xelab/xsim in PATH). "
            "Source your Vivado/cadtools script first."
        )

    # Compile
    _run([xvlog, "-sv"] + abs_sources, cwd=out)

    # Elaborate (debug info required for waveform logging)
    # IMPORTANT: must be '-debug', not 'debug'
    _run([xelab, "-debug", "typical", top, "-snapshot", "work.sim"], cwd=out)

    # Write run.tcl into the run directory
    tcl = (out / "run.tcl").resolve()

    if waves:
        # Most reliable: log everything from root.
        # For small designs (like hello), this is perfect and avoids scope-match warnings.
        tcl_contents = "log_wave -r /\nrun all\nquit\n"
    else:
        tcl_contents = "run all\nquit\n"

    tcl.write_text(tcl_contents, encoding="utf-8")

    if not tcl.is_file():
        raise FileNotFoundError("run.tcl was not created at: %s" % str(tcl))

    # Run simulation in batch; auto-quit on finish/error
    _run(
        [
            xsim,
            "work.sim",
            "-onfinish",
            "quit",
            "-onerror",
            "quit",
            "-tclbatch",
            str(tcl),
        ],
        cwd=out,
    )
