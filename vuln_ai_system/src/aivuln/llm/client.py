from typing import Dict, Optional
import logging
import json
from urllib.request import Request, urlopen

from aivuln.core.models import Finding

LOG = logging.getLogger(__name__)


class LLMReviewer:
    def __init__(self, cfg: Dict[str, object]) -> None:
        self.enabled = bool(cfg.get("enabled", False))
        self.base_url = str(cfg.get("base_url", "")).rstrip("/")
        self.api_key = str(cfg.get("api_key", "EMPTY"))
        self.model = str(cfg.get("model", "Qwen2.5-Coder-7B-Instruct"))
        self.temperature = float(cfg.get("temperature", 0.0))
        self.max_tokens = int(cfg.get("max_tokens", 1024))

    def review(self, finding: Finding) -> Finding:
        if not self.enabled:
            return finding
        prompt = (
            "你是漏洞复核器。只根据证据判断是否保留。"
            "输出 verdict=keep/drop, reason=短句。\n"
            f"type={finding.vuln_type}\nseverity={finding.severity}\n"
            f"confidence={finding.confidence}\nevidence={finding.evidence}\n"
            f"file={finding.file_path}:{finding.line}\n"
        )
        try:
            payload = json.dumps(
                {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "保守复核，证据不足就 drop。"},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
            ).encode("utf-8")
            req = Request(
                f"{self.base_url}/chat/completions",
                data=payload,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=60) as resp:
                content = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
            finding.llm_verdict = content[:500]
            if "verdict=drop" in content.lower():
                finding.confidence = "low"
        except Exception as exc:
            LOG.warning("llm review failed: %s", exc)
            finding.llm_verdict = "review_failed"
        return finding
