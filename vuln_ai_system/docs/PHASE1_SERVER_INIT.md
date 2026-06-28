# 阶段1：服务器初始化环境搭建

## A. 服务器联网阶段

### 1. 建目录

```bash
sudo mkdir -p /opt/aivuln_offline /opt/aivuln
sudo chown -R $USER:$USER /opt/aivuln_offline /opt/aivuln
```

### 2. 执行探测

```bash
bash deploy/offline/phase1/00_env_probe.sh | tee /opt/aivuln_offline/env_probe.log
```

### 3. 准备系统 RPM 缓存

```bash
sudo ROOT_DIR=/opt/aivuln_offline bash deploy/offline/phase1/01_prepare_rpm_cache_online.sh
```

### 4. 放入 Ascend 离线安装包

```bash
mkdir -p /opt/aivuln_offline/ascend_pkgs
ls -lh /opt/aivuln_offline/ascend_pkgs
```

需要放入本地已下载的驱动、CANN toolkit、NNAL、kernels `.run` 包。

### 5. 准备 Python 基础 wheel

```bash
ROOT_DIR=/opt/aivuln_offline PYTHON_BIN=python3.10 bash deploy/offline/phase1/02_prepare_python_wheels_online.sh
```

### 6. 准备 vLLM Ascend wheel

```bash
ROOT_DIR=/opt/aivuln_offline PYTHON_BIN=python3.10 bash deploy/offline/phase1/03_prepare_vllm_ascend_wheels_online.sh
```

### 7. 打包阶段1离线包

```bash
ROOT_DIR=/opt/aivuln_offline OUT=/opt/aivuln_phase1_offline_bundle.tar.gz bash deploy/offline/phase1/04_pack_phase1_bundle.sh
```

## B. 断网前本机离线安装演练

### 1. 禁用联网安装源测试

```bash
sudo /opt/aivuln_offline/install_rpms_offline.sh
sudo ASCEND_PKG_DIR=/opt/aivuln_offline/ascend_pkgs /opt/aivuln_offline/phase1/01b_install_ascend_runtime_offline.sh
APP_DIR=/opt/aivuln PYTHON_BIN=python3.10 /opt/aivuln_offline/install_python_env_offline.sh
APP_DIR=/opt/aivuln /opt/aivuln_offline/install_vllm_ascend_offline.sh
```

### 2. 自检

```bash
APP_DIR=/opt/aivuln bash deploy/offline/phase1/05_offline_selfcheck.sh
```

## C. 断网后恢复安装

### 1. 解包

```bash
sudo mkdir -p /opt
sudo tar xzf aivuln_phase1_offline_bundle.tar.gz -C /opt
sudo chown -R $USER:$USER /opt/aivuln_offline
```

### 2. 安装 RPM

```bash
sudo /opt/aivuln_offline/install_rpms_offline.sh
```

### 3. 安装 Ascend Runtime/CANN

```bash
sudo ASCEND_PKG_DIR=/opt/aivuln_offline/ascend_pkgs /opt/aivuln_offline/phase1/01b_install_ascend_runtime_offline.sh
```

### 4. 创建 Python 环境

```bash
APP_DIR=/opt/aivuln PYTHON_BIN=python3.10 /opt/aivuln_offline/install_python_env_offline.sh
```

### 5. 安装 vLLM Ascend

```bash
APP_DIR=/opt/aivuln /opt/aivuln_offline/install_vllm_ascend_offline.sh
```

### 6. 自检

```bash
APP_DIR=/opt/aivuln /opt/aivuln_offline/phase1/05_offline_selfcheck.sh
```
