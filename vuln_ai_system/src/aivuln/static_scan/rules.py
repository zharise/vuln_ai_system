import re


RULES = [
    {
        "id": "py-subprocess-shell-true",
        "ext": [".py"],
        "type": "Command Injection",
        "severity": "high",
        "confidence": "medium",
        "pattern": re.compile(r"subprocess\.(Popen|run|call|check_output)\([^\n]*shell\s*=\s*True"),
        "recommendation": "避免 shell=True；使用参数数组并对白名单参数做校验。",
    },
    {
        "id": "py-sql-string-format",
        "ext": [".py"],
        "type": "SQL Injection",
        "severity": "high",
        "confidence": "medium",
        "pattern": re.compile(r"(execute|executemany)\([^\n]*(%|\.format\(|f[\"'])"),
        "recommendation": "使用参数化查询，不拼接 SQL。",
    },
    {
        "id": "php-request-sql-concat",
        "ext": [".php"],
        "type": "SQL Injection",
        "severity": "high",
        "confidence": "medium",
        "pattern": re.compile(r"(mysqli_query|mysql_query|PDO::query)\s*\([^\n]*(\$_GET|\$_POST|\$_REQUEST)"),
        "recommendation": "使用 prepared statement 并绑定参数。",
    },
    {
        "id": "java-runtime-exec-tainted",
        "ext": [".java"],
        "type": "Command Injection",
        "severity": "high",
        "confidence": "medium",
        "pattern": re.compile(r"Runtime\.getRuntime\(\)\.exec\s*\([^\n]*(request|getParameter|args)"),
        "recommendation": "禁止用户输入直接进入命令执行；使用白名单和固定命令模板。",
    },
    {
        "id": "c-dangerous-copy",
        "ext": [".c", ".h", ".cc", ".cpp"],
        "type": "Memory Safety",
        "severity": "medium",
        "confidence": "low",
        "pattern": re.compile(r"\b(strcpy|strcat|sprintf|gets)\s*\("),
        "recommendation": "替换为有边界检查的 API，并验证目标缓冲区长度。",
    },
    {
        "id": "hardcoded-secret",
        "ext": [".py", ".java", ".php", ".c", ".h", ".cpp", ".cc"],
        "type": "Hardcoded Secret",
        "severity": "medium",
        "confidence": "medium",
        "pattern": re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
        "recommendation": "将密钥迁移到离线密钥管理或环境变量，立即轮换已泄露密钥。",
    },
]

