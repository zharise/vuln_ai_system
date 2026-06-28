from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class Finding:
    source: str
    target: str
    vuln_type: str
    severity: str
    confidence: str
    evidence: str
    recommendation: str
    file_path: str = ""
    line: int = 0
    end_line: int = 0
    poc: str = ""
    llm_verdict: str = "not_reviewed"
    fingerprint: str = ""
    created_at: str = ""

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        if not data["end_line"]:
            data["end_line"] = data["line"]
        if not data["created_at"]:
            data["created_at"] = datetime.now(timezone.utc).isoformat()
        return data


@dataclass
class ScanContext:
    project_root: str
    run_dir: str
    config: Dict[str, object]
