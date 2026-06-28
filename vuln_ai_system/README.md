# 阶段1 MVP：AI漏洞挖掘系统

## 目录结构

```text
vuln_ai_system/
  config/system.yaml
  requirements.txt
  requirements-vllm-ascend.txt
  src/aivuln/
    cli.py
    api.py
    core/
    static_scan/
    dynamic_scan/
    llm/
    output/
  scripts/
    run_once.sh
    start_vllm.sh
    start_api.sh
    start_all.sh
    stop_all.sh
    install_offline.sh
    install_systemd.sh
    pack_offline.sh
    download_vllm_ascend_wheels.sh
  deploy/
    systemd/
    docker/
  data/
    source/
    targets/
    runs/
  models/
  wheelhouse/
```

## 输入

源码：

```bash
cp -a /data/competition/source/* data/source/
```

在线目标：

```bash
cat > data/targets/targets.txt <<'EOF'
http://192.168.1.10:8080
http://192.168.1.11:8000
EOF
```

## 一步启动扫描

```bash
cd /opt/aivuln
source .venv/bin/activate
./scripts/run_once.sh
```

## 输出

```text
data/runs/latest/source_vuln_result.xlsx
data/runs/latest/online_vuln_result.xlsx
data/runs/latest/findings.jsonl
data/runs/latest/run.log
```

源码类 Excel 字段：

```text
file_path, has_vuln, start_line, end_line, poc
```

在线服务类 Excel 字段：

```text
target_url, poc
```

## vLLM + Qwen 最简启动

```bash
cd /opt/aivuln
source .venv/bin/activate
export MODEL_PATH=/opt/aivuln/models/Qwen2.5-Coder-7B-Instruct
./scripts/start_vllm.sh
```

启用模型复核：

```bash
python3 - <<'PY'
from pathlib import Path
p = Path("config/system.yaml")
s = p.read_text()
s = s.replace("enabled: false", "enabled: true", 1)
p.write_text(s)
PY
./scripts/run_once.sh
```

## 离线安装

联网构建机：

```bash
./scripts/pack_offline.sh
./scripts/download_vllm_ascend_wheels.sh
tar czf offline_bundle/aivuln_full_offline_bundle.tar.gz \
  config src scripts deploy docs requirements.txt requirements-vllm-ascend.txt \
  wheelhouse wheelhouse-vllm-ascend models data/source data/targets
```

openEuler 22.03 离线机器：

```bash
mkdir -p /opt/aivuln
tar xzf aivuln_full_offline_bundle.tar.gz -C /opt/aivuln
cd /opt/aivuln
./scripts/install_offline.sh
./scripts/run_once.sh
```
