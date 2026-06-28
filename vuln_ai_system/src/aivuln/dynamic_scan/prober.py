from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Iterable, List
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import hashlib
import logging

from aivuln.core.models import Finding

LOG = logging.getLogger(__name__)


def load_targets(path: str) -> List[str]:
    targets = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                item = line.strip()
                if item and not item.startswith("#"):
                    targets.append(item)
    except FileNotFoundError:
        LOG.warning("targets file not found: %s", path)
    return targets


def _probe_one(target: str, paths: Iterable[str], headers: Dict[str, str], timeout: int) -> List[Finding]:
    findings: List[Finding] = []
    for path in paths:
        url = urljoin(target.rstrip("/") + "/", path.lstrip("/"))
        try:
            req = Request(url, headers=headers, method="GET")
            with urlopen(req, timeout=timeout) as resp:
                status = resp.status
                resp_headers = dict(resp.headers.items())
                body = resp.read(4096).decode("utf-8", errors="ignore").lower()
        except HTTPError as exc:
            status = exc.code
            resp_headers = dict(exc.headers.items())
            body = exc.read(4096).decode("utf-8", errors="ignore").lower()
        except (URLError, TimeoutError, ValueError) as exc:
            LOG.info("probe failed %s: %s", url, exc)
            continue
        server = resp_headers.get("Server", "")
        powered = resp_headers.get("X-Powered-By", "")
        if path == "/phpinfo.php" and "phpinfo()" in body and "php version" in body:
            evidence = f"GET {url} status={status} body contains phpinfo markers"
            findings.append(_finding(target, "Exposed phpinfo", "high", "high", evidence, "删除 phpinfo.php 或限制访问。"))
        if path == "/server-status" and status == 200 and "apache server status" in body:
            evidence = f"GET {url} status=200 body contains Apache server-status marker"
            findings.append(_finding(target, "Exposed Server Status", "medium", "high", evidence, "关闭 server-status 或限制管理网段访问。"))
        if path.startswith("/actuator") and status == 200 and ("status" in body and ("up" in body or "diskspace" in body)):
            evidence = f"GET {url} status=200 body contains actuator health markers"
            findings.append(_finding(target, "Exposed Spring Actuator", "medium", "medium", evidence, "限制 actuator 访问并关闭不必要端点。"))
        if server or powered:
            LOG.info("fingerprint %s server=%s x-powered-by=%s", target, server, powered)
    return findings


def _finding(target: str, vuln_type: str, severity: str, confidence: str, evidence: str, recommendation: str) -> Finding:
    fp = hashlib.sha256(f"dynamic:{target}:{vuln_type}:{evidence}".encode()).hexdigest()[:16]
    return Finding(
        source="dynamic",
        target=target,
        vuln_type=vuln_type,
        severity=severity,
        confidence=confidence,
        evidence=evidence,
        recommendation=recommendation,
        fingerprint=fp,
        poc=evidence,
    )


def scan_dynamic(targets_file: str, cfg: Dict[str, object], max_workers: int, timeout: int) -> List[Finding]:
    if not cfg.get("enabled", True):
        return []
    targets = load_targets(targets_file)
    paths = cfg.get("http_paths", ["/"])
    headers = cfg.get("low_noise_headers", {})
    findings: List[Finding] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(_probe_one, t, paths, headers, timeout) for t in targets]
        for fut in as_completed(futures):
            findings.extend(fut.result())
    LOG.info("dynamic findings: %d", len(findings))
    return findings
