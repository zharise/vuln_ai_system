from datetime import datetime
from pathlib import Path
import argparse
import logging
import shutil

from aivuln.core.config import load_config
from aivuln.core.logging import setup_logging
from aivuln.dynamic_scan.prober import scan_dynamic
from aivuln.llm.client import LLMReviewer
from aivuln.output.excel import write_outputs
from aivuln.static_scan.scanner import scan_static

LOG = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/system.yaml")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--dynamic-only", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    root = Path(cfg["runtime"]["project_root"]).resolve()
    run_id = args.run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = root / cfg["runtime"]["runs_dir"] / run_id
    latest_dir = root / cfg["runtime"]["runs_dir"] / "latest"
    setup_logging(str(run_dir))

    findings = []
    if not args.dynamic_only:
        findings.extend(scan_static(str(root / cfg["runtime"]["source_dir"]), cfg["static_scan"]))
    if not args.static_only:
        findings.extend(
            scan_dynamic(
                str(root / cfg["runtime"]["targets_file"]),
                cfg["dynamic_scan"],
                int(cfg["runtime"]["max_workers"]),
                int(cfg["runtime"]["request_timeout_sec"]),
            )
        )

    reviewer = LLMReviewer(cfg["llm"])
    reviewed = [reviewer.review(f) for f in findings]
    reviewed = [f for f in reviewed if not (f.llm_verdict.lower().startswith("verdict=drop"))]

    write_outputs(
        reviewed,
        str(run_dir),
        cfg["output"]["source_excel_file"],
        cfg["output"]["online_excel_file"],
        cfg["output"]["jsonl_file"],
    )
    if latest_dir.exists() or latest_dir.is_symlink():
        if latest_dir.is_symlink():
            latest_dir.unlink()
        else:
            shutil.rmtree(latest_dir)
    shutil.copytree(run_dir, latest_dir)
    LOG.info("run complete: %s findings=%d", run_dir, len(reviewed))


if __name__ == "__main__":
    main()
