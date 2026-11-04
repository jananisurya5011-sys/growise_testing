import os
import sys
import zipfile
from xml.sax.saxutils import escape

# Try importing openpyxl first; if unavailable, fallback to pure-Python zipfile XLSX writer
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class PureXlsxWriter:
    """
    Pure Python XLSX Generator that uses standard zipfile + OpenXML standards.
    Requires ZERO external packages. Produces 100% valid Excel workbooks.
    """
    def __init__(self, filename):
        self.filename = filename
        self.sheets = []  # list of (sheet_name, rows_data)

    def add_sheet(self, sheet_name, rows):
        """rows is a list of lists representing rows of cells."""
        clean_name = sheet_name.replace("/", "_").replace("\\", "_").replace("?", "_").replace("*", "_")[:31]
        self.sheets.append((clean_name, rows))

    def save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.filename)), exist_ok=True)
        with zipfile.ZipFile(self.filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', self._build_content_types())
            zf.writestr('_rels/.rels', self._build_root_rels())
            zf.writestr('xl/workbook.xml', self._build_workbook())
            zf.writestr('xl/_rels/workbook.xml.rels', self._build_workbook_rels())
            zf.writestr('xl/styles.xml', self._build_styles())
            for idx, (name, rows) in enumerate(self.sheets, start=1):
                zf.writestr(f'xl/worksheets/sheet{idx}.xml', self._build_sheet(rows))

    def _build_content_types(self):
        sheets_xml = "".join([f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(self.sheets) + 1)])
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
    {sheets_xml}
</Types>'''

    def _build_root_rels(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

    def _build_workbook(self):
        sheets_tags = "".join([f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i, (name, _) in enumerate(self.sheets, start=1)])
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        {sheets_tags}
    </sheets>
</workbook>'''

    def _build_workbook_rels(self):
        rels = []
        for i in range(1, len(self.sheets) + 1):
            rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>')
        styles_id = f'rId{len(self.sheets) + 1}'
        rels.append(f'<Relationship Id="{styles_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    {"".join(rels)}
</Relationships>'''

    def _build_styles(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="3">
        <font><sz val="11"/><name val="Calibri"/></font>
        <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
        <font><b/><sz val="11"/><color rgb="FF1F2937"/><name val="Calibri"/></font>
    </fonts>
    <fills count="5">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFFEE2E2"/></patternFill></fill>
    </fills>
    <borders count="2">
        <border><left/><right/><top/><bottom/></border>
        <border>
            <left style="thin"><color rgb="FFD1D5DB"/></left>
            <right style="thin"><color rgb="FFD1D5DB"/></right>
            <top style="thin"><color rgb="FFD1D5DB"/></top>
            <bottom style="thin"><color rgb="FFD1D5DB"/></bottom>
        </border>
    </borders>
    <cellStyleXfs count="1">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
    </cellStyleXfs>
    <cellXfs count="5">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="2" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1"/>
    </cellXfs>
</styleSheet>'''

    def _col_letter(self, col_idx):
        result = ""
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            result = chr(65 + remainder) + result
        return result

    def _build_sheet(self, rows):
        sheet_rows = []
        max_cols = 0
        for r_idx, row in enumerate(rows, start=1):
            cell_xmls = []
            max_cols = max(max_cols, len(row))
            for c_idx, val in enumerate(row, start=1):
                col_let = self._col_letter(c_idx)
                cell_ref = f"{col_let}{r_idx}"
                str_val = "" if val is None else str(val)
                
                style_idx = 0
                if r_idx == 1:
                    style_idx = 1 # Header
                elif str_val == "PASS":
                    style_idx = 2
                elif str_val in ["FAIL", "BLOCKED"]:
                    style_idx = 3
                elif c_idx == 1 and len(row) == 2:
                    style_idx = 4
                
                try:
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        cell_xmls.append(f'<c r="{cell_ref}" s="{style_idx}"><v>{val}</v></c>')
                    else:
                        cell_xmls.append(f'<c r="{cell_ref}" t="inlineStr" s="{style_idx}"><is><t>{escape(str_val)}</t></is></c>')
                except Exception:
                    cell_xmls.append(f'<c r="{cell_ref}" t="inlineStr" s="{style_idx}"><is><t>{escape(str_val)}</t></is></c>')
            sheet_rows.append(f'<row r="{r_idx}">{"".join(cell_xmls)}</row>')

        cols_def = []
        for c in range(1, max_cols + 1):
            cols_def.append(f'<col min="{c}" max="{c}" width="22" customWidth="1"/>')
        cols_xml = f'<cols>{"".join(cols_def)}</cols>' if cols_def else ''

        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    {cols_xml}
    <sheetData>
        {"".join(sheet_rows)}
    </sheetData>
</worksheet>'''


def create_excel_report(filepath, summary_dict, results_records, category_sheets=None, custom_headers=None):
    """
    Standardized multi-sheet Excel report builder.
    Supports openpyxl when present, falling back to PureXlsxWriter seamlessly.
    """
    if custom_headers:
        headers = custom_headers
    else:
        headers = [
            "Test ID",
            "Test Category",
            "Test Name",
            "Objective",
            "Preconditions",
            "Steps",
            "Test Data",
            "Expected Result",
            "Actual Result",
            "Status",
            "Priority",
            "Severity",
            "Execution Time",
            "Error/Failure Message",
            "Screenshot/Artifact",
            "Remarks",
            "Automation Status"
        ]

    summary_rows = [
        ["FIELD", "VALUE"],
        ["Suite Title", summary_dict.get("title", "Quality Test Report")],
        ["Category", summary_dict.get("category", "General")],
        ["Total Tests", summary_dict.get("total", len(results_records))],
        ["Passed", summary_dict.get("passed", sum(1 for r in results_records if r.get("Status") == "PASS"))],
        ["Failed", summary_dict.get("failed", sum(1 for r in results_records if r.get("Status") == "FAIL"))],
        ["Skipped", summary_dict.get("skipped", 0)],
        ["Blocked", summary_dict.get("blocked", 0)],
        ["Pass Percentage", f"{summary_dict.get('pass_rate', 100.0):.2f}%"],
        ["Execution Time", summary_dict.get("execution_time", "0.00s")],
        ["Environment", summary_dict.get("environment", "CI/CD GitHub Actions")],
        ["Build/Commit", summary_dict.get("build_commit", "main-latest")],
        ["Timestamp", summary_dict.get("timestamp", "2026-11-04T00:00:00Z")],
        ["Deployment Readiness", summary_dict.get("deployment_readiness", "PASS")]
    ]

    # Include extra performance/load metrics if present
    if "min_response_time" in summary_dict:
        summary_rows.append(["Min Response Time", summary_dict["min_response_time"]])
    if "max_response_time" in summary_dict:
        summary_rows.append(["Max Response Time", summary_dict["max_response_time"]])
    if "avg_response_time" in summary_dict:
        summary_rows.append(["Avg Response Time", summary_dict["avg_response_time"]])
    if "total_requests" in summary_dict:
        summary_rows.append(["Total Requests", summary_dict["total_requests"]])
    if "time_period" in summary_dict:
        summary_rows.append(["Time Period", summary_dict["time_period"]])
    if "throughput_rps" in summary_dict:
        summary_rows.append(["Throughput (RPS)", summary_dict["throughput_rps"]])

    results_rows = [headers]
    for r in results_records:
        row = [r.get(h, "") for h in headers]
        results_rows.append(row)

    if HAS_OPENPYXL:
        wb = openpyxl.Workbook()
        ws_summary = wb.active
        ws_summary.title = "SUMMARY"
        for r in summary_rows:
            ws_summary.append(r)
        
        ws_results = wb.create_sheet("TEST RESULTS")
        for r in results_rows:
            ws_results.append(r)
            
        if category_sheets:
            for cat in category_sheets:
                cat_rows = [headers]
                for r in results_records:
                    if r.get("Test Category", "").upper() == cat.upper() or cat.upper() in r.get("Test Category", "").upper():
                        cat_rows.append([r.get(h, "") for h in headers])
                if len(cat_rows) > 1:
                    ws_cat = wb.create_sheet(cat[:31])
                    for r in cat_rows:
                        ws_cat.append(r)

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wb.save(filepath)
    else:
        writer = PureXlsxWriter(filepath)
        writer.add_sheet("SUMMARY", summary_rows)
        writer.add_sheet("TEST RESULTS", results_rows)
        
        if category_sheets:
            for cat in category_sheets:
                cat_rows = [headers]
                for r in results_records:
                    if r.get("Test Category", "").upper() == cat.upper() or cat.upper() in r.get("Test Category", "").upper():
                        cat_rows.append([r.get(h, "") for h in headers])
                if len(cat_rows) > 1:
                    writer.add_sheet(cat[:31], cat_rows)
                    
        writer.save()

    return filepath
