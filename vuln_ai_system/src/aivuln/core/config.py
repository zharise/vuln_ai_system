from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_config(path: str) -> Dict[str, Any]:
    cfg_path = Path(path)
    with cfg_path.open("r", encoding="utf-8") as f:
        if yaml:
            return yaml.safe_load(f)
        return _load_simple_yaml(f.read())


def _load_simple_yaml(text: str) -> Dict[str, Any]:
    lines = [
        (len(raw) - len(raw.lstrip(" ")), raw.strip())
        for raw in text.splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    data, _ = _parse_map(lines, 0, 0)
    return data


def _parse_map(lines: list, idx: int, indent: int) -> tuple:
    data: Dict[str, Any] = {}
    while idx < len(lines):
        cur_indent, line = lines[idx]
        if cur_indent < indent:
            break
        if cur_indent > indent:
            idx += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = _parse_scalar(value)
            idx += 1
            continue
        next_idx = idx + 1
        if next_idx < len(lines) and lines[next_idx][1].startswith("- "):
            data[key], idx = _parse_list(lines, next_idx, lines[next_idx][0])
        else:
            data[key], idx = _parse_map(lines, next_idx, indent + 2)
    return data, idx


def _parse_list(lines: list, idx: int, indent: int) -> tuple:
    items = []
    while idx < len(lines):
        cur_indent, line = lines[idx]
        if cur_indent != indent or not line.startswith("- "):
            break
        items.append(_parse_scalar(line[2:]))
        idx += 1
    return items, idx


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value
