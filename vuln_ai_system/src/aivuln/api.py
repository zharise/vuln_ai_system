from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

app = FastAPI(title="AI Vulnerability Mining API", version="0.1.0")


class ScanRequest(BaseModel):
    config: str = "config/system.yaml"
    mode: str = "all"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/scan")
def scan(req: ScanRequest) -> dict:
    cmd = [sys.executable, "-m", "aivuln.cli", "--config", req.config]
    if req.mode == "static":
        cmd.append("--static-only")
    if req.mode == "dynamic":
        cmd.append("--dynamic-only")
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=24 * 3600)
    return {"returncode": proc.returncode, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-4000:]}

