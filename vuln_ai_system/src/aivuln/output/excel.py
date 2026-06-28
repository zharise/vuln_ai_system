from pathlib import Path
from typing import Iterable, List
import json
import html
import zipfile

from aivuln.core.models import Finding


SOURCE_HEADERS = ["file_path", "has_vuln", "start_line", "end_line", "poc"]
ONLINE_HEADERS = ["target_url", "poc"]
JSONL_HEADERS = [
    "source", "target", "vuln_type", "severity", "confidence", "file_path",
    "line", "end_line", "evidence", "poc", "recommendation", "llm_verdict", "fingerprint", "created_at",
]


def write_outputs(
    findings: Iterable[Finding],
    run_dir: str,
    source_excel_name: str,
    online_excel_name: str,
    jsonl_name: str,
) -> None:
    rows = [f.to_dict() for f in findings]
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    with (Path(run_dir) / jsonl_name).open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    source_rows = [
        {
            "file_path": row.get("file_path") or row.get("target", ""),
            "has_vuln": "Yes",
            "start_line": row.get("line", 0),
            "end_line": row.get("end_line") or row.get("line", 0),
            "poc": row.get("poc") or row.get("evidence", ""),
        }
        for row in rows
        if row.get("source") == "static"
    ]
    online_rows = [
        {
            "target_url": row.get("target", ""),
            "poc": row.get("poc") or row.get("evidence", ""),
        }
        for row in rows
        if row.get("source") == "dynamic"
    ]
    _write_excel(source_rows, Path(run_dir) / source_excel_name, SOURCE_HEADERS)
    _write_excel(online_rows, Path(run_dir) / online_excel_name, ONLINE_HEADERS)


def _write_excel(rows: List[dict], path: Path, headers: List[str]) -> None:
    sheet_rows = [headers] + [[str(row.get(h, "")) for h in headers] for row in rows]
    sheet_xml = _sheet_xml(sheet_rows)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", RELS)
        zf.writestr("xl/workbook.xml", WORKBOOK)
        zf.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def _sheet_xml(rows: List[List[str]]) -> str:
    xml_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            ref = f"{_col(c_idx)}{r_idx}"
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{html.escape(value)}</t></is></c>')
        xml_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        '<autoFilter ref="A1:Z1048576"/>'
        '</worksheet>'
    )


def _col(idx: int) -> str:
    name = ""
    while idx:
        idx, rem = divmod(idx - 1, 26)
        name = chr(65 + rem) + name
    return name


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

WORKBOOK = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="findings" sheetId="1" r:id="rId1"/></sheets>
</workbook>'''

WORKBOOK_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''
