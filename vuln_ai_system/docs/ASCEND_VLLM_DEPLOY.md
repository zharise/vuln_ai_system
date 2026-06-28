# Ascend B2x2 / openEuler 22.03 部署

## 1. 目录

```bash
sudo mkdir -p /opt/aivuln
sudo cp -a vuln_ai_system/* /opt/aivuln/
cd /opt/aivuln
```

## 2. Python 环境

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links wheelhouse -r requirements.txt
pip install --no-index --find-links wheelhouse-vllm-ascend -r requirements-vllm-ascend.txt
```

## 3. 模型目录

```bash
mkdir -p /opt/aivuln/models/Qwen2.5-Coder-7B-Instruct
# 将离线模型文件放入上面目录，至少包含 config.json tokenizer* model*.safetensors
```

## 4. 启动

```bash
chmod +x scripts/*.sh
MODEL_PATH=/opt/aivuln/models/Qwen2.5-Coder-7B-Instruct ./scripts/start_vllm.sh
```

另开终端：

```bash
./scripts/start_api.sh
```

扫描：

```bash
./scripts/run_once.sh
ls -lh data/runs/latest/source_vuln_result.xlsx data/runs/latest/online_vuln_result.xlsx
```

## 5. systemd

```bash
sudo ./scripts/install_systemd.sh
sudo systemctl start aivuln-vllm
sudo systemctl start aivuln-api
```

## 6. 离线打包

在联网构建机：

```bash
./scripts/pack_offline.sh
./scripts/download_vllm_ascend_wheels.sh
tar czf offline_bundle/aivuln_full_offline_bundle.tar.gz \
  config src scripts deploy docs requirements.txt requirements-vllm-ascend.txt \
  wheelhouse wheelhouse-vllm-ascend models data/targets/targets.example.txt
```
