from pathlib import Path
from typing import Dict, Iterable, List
import hashlib
import logging

from aivuln.core.models import Finding
from aivuln.static_scan.rules import RULES

LOG = logging.getLogger(__name__)


CONF_ORDER = {"low": 1, "medium": 2, "high": 3}


def iter_source_files(root: str, include_ext: Iterable[str], max_size_mb: int) -> Iterable[Path]:
    base = Path(root)
    if not base.exists():
        LOG.warning("source_dir not found: %s", root)
        return
    max_size = max_size_mb * 1024 * 1024
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in include_ext and path.stat().st_size <= max_size:
            yield path


def scan_static(source_dir: str, cfg: Dict[str, object]) -> List[Finding]:
    include_ext = set(cfg["include_ext"])
    min_conf = str(cfg.get("min_confidence", "medium"))
    findings: List[Finding] = []
    for path in iter_source_files(source_dir, include_ext, int(cfg.get("max_file_size_mb", 5))):
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        for rule in RULES:
            if path.suffix.lower() not in rule["ext"]:
                continue
            if CONF_ORDER[rule["confidence"]] < CONF_ORDER[min_conf]:
                continue
            for idx, line in enumerate(lines, start=1):
                if rule["pattern"].search(line):
                    evidence = line.strip()[:500]
                    fp = hashlib.sha256(f"{rule['id']}:{path}:{idx}:{evidence}".encode()).hexdigest()[:16]
                    findings.append(
                        Finding(
                            source="static",
                            target=str(path),
                            file_path=str(path),
                            line=idx,
                            end_line=idx,
                            vuln_type=rule["type"],
                            severity=rule["severity"],
                            confidence=rule["confidence"],
                            evidence=evidence,
                            recommendation=rule["recommendation"],
                            poc=f"{rule['type']} candidate at {path}:{idx}; evidence: {evidence}",
                            fingerprint=fp,
                        )
                    )
    LOG.info("static findings: %d", len(findings))
    return findings
