"""
Convert report_zh.md → report_zh.docx
Style: academic research report (per typography_guide.md + cjk_typography.md)
- Body: Times New Roman 12pt (Latin) + SimSun 12pt (CJK)
- Line spacing: 1.5 (academic reports)
- Page: A4, 1in margins, page numbers bottom center
- Headings: same font, bold, black
- Tables: three-line (academic standard)
- Images: centered with caption
- Code: Consolas 10pt, light gray background
- LaTeX formulas: italic Cambria Math fallback
"""

import re
import sys
from pathlib import Path
from copy import deepcopy

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement


# Paths
WORKSPACE = Path(r"D:\ProjectforMM\IA_Finance_MA01")
MD_PATH = WORKSPACE / "reports" / "report_zh.md"
DOCX_PATH = WORKSPACE / "reports" / "report_zh.docx"
FIGURES_DIR = WORKSPACE / "figures"


# ────────────────────────────────────────────────────────────────────
# Helpers — OOXML low-level
# ────────────────────────────────────────────────────────────────────

def _set_cn_font(run, ascii_font, eastasia_font):
    """Set both Western (ascii/hAnsi) and CJK (eastAsia) fonts on a run."""
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), ascii_font)
    rFonts.set(qn("w:hAnsi"), ascii_font)
    rFonts.set(qn("w:eastAsia"), eastasia_font)
    rFonts.set(qn("w:cs"), ascii_font)


def _set_paragraph_spacing(para, before_pt=None, after_pt=None, line=1.5, line_rule="multiple"):
    pPr = para._element.get_or_add_pPr()
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    if before_pt is not None:
        spacing.set(qn("w:before"), str(int(before_pt * 20)))
    if after_pt is not None:
        spacing.set(qn("w:after"), str(int(after_pt * 20)))
    if line_rule == "multiple":
        spacing.set(qn("w:line"), str(int(line * 240)))
        spacing.set(qn("w:lineRule"), "auto")
    elif line_rule == "exact":
        spacing.set(qn("w:line"), str(int(line * 20)))
        spacing.set(qn("w:lineRule"), "exact")


def _add_shading(para_or_cell, fill_hex):
    """Add background shading (e.g., for code blocks)."""
    pPr = para_or_cell._element.get_or_add_pPr() if hasattr(para_or_cell, '_element') else None
    if pPr is None:
        # Table cell
        tcPr = para_or_cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill_hex)
        # remove existing
        for old in tcPr.findall(qn("w:shd")):
            tcPr.remove(old)
        tcPr.append(shd)
        return
    shd = pPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        pPr.append(shd)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)


def _set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Set per-cell borders. Each value is dict {sz, color} or None to skip."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is not None:
        tcPr.remove(tcBorders)
    tcBorders = OxmlElement("w:tcBorders")
    for name, spec in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        if spec is None:
            b = OxmlElement(f"w:{name}")
            b.set(qn("w:val"), "nil")
            tcBorders.append(b)
        else:
            b = OxmlElement(f"w:{name}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), str(spec.get("sz", 4)))
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), spec.get("color", "000000"))
            tcBorders.append(b)
    tcPr.append(tcBorders)


def _add_page_number(footer_para):
    """Insert PAGE field."""
    run = footer_para.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    run._element.append(fldChar1)

    run2 = footer_para.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE \\* MERGEFORMAT "
    run2._element.append(instr)

    run3 = footer_para.add_run()
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run3._element.append(fldChar3)


def _add_run_with_cn_font(para, text, ascii_font="Times New Roman", eastasia_font="SimSun",
                          size_pt=12, bold=False, italic=False, color=None):
    """Add a run with explicit CJK font + size, supporting inline **bold**, *italic*, and [^N] footnote refs."""
    # First split on footnote markers [^N] so we can insert Word footnote references
    fn_parts = re.split(r"(\[\^\d+\])", text)
    for fn_part in fn_parts:
        if not fn_part:
            continue
        fm = re.match(r"^\[\^(\d+)\]$", fn_part)
        if fm:
            # Footnote reference — insert [N] with a Word footnote inside
            _add_footnote_reference_brackets(para, int(fm.group(1)), size_pt=size_pt,
                                              ascii_font=ascii_font, eastasia_font=eastasia_font)
            continue
        # Otherwise, split this segment on bold/italic markers
        parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", fn_part)
        for part in parts:
            if not part:
                continue
            is_bold = part.startswith("**") and part.endswith("**")
            is_italic = part.startswith("*") and part.endswith("*") and not is_bold
            clean = part.strip("*").strip()
            if not clean:
                continue
            run = para.add_run(clean)
            run.font.size = Pt(size_pt)
            _set_cn_font(run, ascii_font, eastasia_font)
            if bold or is_bold:
                run.bold = True
            if italic or is_italic:
                run.italic = True
            if color:
                run.font.color.rgb = RGBColor.from_string(color)


def _add_footnote_reference_brackets(para, fn_id, size_pt=12, ascii_font="Times New Roman",
                                      eastasia_font="SimSun"):
    """Insert a Word footnote reference wrapped in literal [N] brackets.

    Renders as "[¹]" — the brackets are regular text and the digit is the
    auto-numbered Word footnote marker (superscript).
    """
    # Open bracket "["
    ob = para.add_run("[")
    ob.font.size = Pt(size_pt)
    _set_cn_font(ob, ascii_font, eastasia_font)
    # The actual Word footnote reference (auto-numbered, superscript)
    ref_run = para.add_run()
    rPr = ref_run._element.get_or_add_rPr()
    rStyle = OxmlElement("w:rStyle")
    rStyle.set(qn("w:val"), "FootnoteReference")
    rPr.insert(0, rStyle)
    # Slight size reduction for the marker
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size_pt * 1.6)))  # 字号 半点单位
    rPr.append(sz)
    fnRef = OxmlElement("w:footnoteReference")
    fnRef.set(qn("w:id"), str(fn_id))
    ref_run._element.append(fnRef)
    # Close bracket "]"
    cb = para.add_run("]")
    cb.font.size = Pt(size_pt)
    _set_cn_font(cb, ascii_font, eastasia_font)


# ────────────────────────────────────────────────────────────────────
# Document setup — page, styles, default font
# ────────────────────────────────────────────────────────────────────

def setup_document():
    doc = Document()

    # Page setup — A4, 1in margins
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # Document defaults — CJK + Latin fonts
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    rpr = normal.element.get_or_add_rPr()
    rFonts = rpr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rpr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "SimSun")
    rFonts.set(qn("w:cs"), "Times New Roman")

    # Body paragraph default spacing
    pPr_default = OxmlElement("w:pPr")
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:line"), "360")  # 1.5 line
    spacing.set(qn("w:lineRule"), "auto")
    spacing.set(qn("w:after"), "120")
    pPr_default.append(spacing)
    # Remove any default pPr to avoid duplicates
    for old in normal.element.findall(qn("w:pPr")):
        normal.element.remove(old)
    normal.element.append(pPr_default)

    # Heading styles — institutional blue, bold, decreasing size (primary visual hierarchy)
    heading_sizes = {1: 18, 2: 16, 3: 14, 4: 12, 5: 12, 6: 11}
    for level in range(1, 7):
        style = styles[f"Heading {level}"]
        style.font.name = "Times New Roman"
        style.font.bold = True
        # Slightly lighter blue for deeper levels
        if level <= 2:
            style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)  # institutional dark blue
        else:
            style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)  # mid blue
        size_pt = heading_sizes[level]
        style.font.size = Pt(size_pt)
        rpr = style.element.get_or_add_rPr()
        rFonts = rpr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rpr.insert(0, rFonts)
        rFonts.set(qn("w:ascii"), "Times New Roman")
        rFonts.set(qn("w:hAnsi"), "Times New Roman")
        rFonts.set(qn("w:eastAsia"), "SimHei")
        rFonts.set(qn("w:cs"), "Times New Roman")

    # Footer — page number bottom center
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_page_number(fp)

    # Header — report short title (can be overridden via _HEADER_TEXT)
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = hp.add_run(_HEADER_TEXT)
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    _set_cn_font(run, "Times New Roman", "SimSun")

    return doc


# ────────────────────────────────────────────────────────────────────
# Element builders
# ────────────────────────────────────────────────────────────────────

def add_title(doc, text, size_pt=28):
    """Document main title — large, bold, institutional blue."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_paragraph_spacing(p, before_pt=24, after_pt=12, line=1.5)
    _add_run_with_cn_font(p, text, size_pt=size_pt, bold=True, color="1F4E79")
    return p


def add_subtitle(doc, text, size_pt=13):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_paragraph_spacing(p, after_pt=18, line=1.5)
    _add_run_with_cn_font(p, text, size_pt=size_pt, color="606060")
    return p


def add_abstract(doc, label, body):
    """Abstract block: bold '摘要.' label + body, indented both sides, justified."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.left_indent = Cm(0.75)
    pf.right_indent = Cm(0.75)
    _set_paragraph_spacing(p, before_pt=6, after_pt=12, line=1.5)
    _add_run_with_cn_font(p, f"{label} ", size_pt=11, bold=True)
    _add_run_with_cn_font(p, body, size_pt=11)
    return p


def add_keywords(doc, body):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.left_indent = Cm(0.75)
    pf.right_indent = Cm(0.75)
    _set_paragraph_spacing(p, before_pt=0, after_pt=18, line=1.5)
    _add_run_with_cn_font(p, "**关键词**", size_pt=11, bold=True)
    _add_run_with_cn_font(p, "：" + body, size_pt=11)
    return p


def add_heading(doc, text, level):
    level = max(1, min(level, 6))
    p = doc.add_paragraph(style=f"Heading {level}")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if level == 1:
        _set_paragraph_spacing(p, before_pt=18, after_pt=10, line=1.5)
    elif level == 2:
        _set_paragraph_spacing(p, before_pt=14, after_pt=8, line=1.5)
    elif level == 3:
        _set_paragraph_spacing(p, before_pt=10, after_pt=6, line=1.5)
    else:
        _set_paragraph_spacing(p, before_pt=8, after_pt=4, line=1.5)
    heading_sizes = {1: 16, 2: 14, 3: 12, 4: 12, 5: 11, 6: 11}
    size_pt = heading_sizes[level]
    # Level 4+ gets italic + indent to differentiate from body
    is_sub = level >= 4
    _add_run_with_cn_font(p, text, size_pt=size_pt, bold=True, italic=is_sub)
    return p


def add_paragraph(doc, text, first_line_indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if first_line_indent:
        p.paragraph_format.first_line_indent = Cm(0.74)  # ~2 Chinese chars at 12pt
    _set_paragraph_spacing(p, after_pt=4, line=1.5)
    _add_run_with_cn_font(p, text, size_pt=12)
    return p


def add_blockquote(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.left_indent = Cm(0.6)
    pf.right_indent = Cm(0.6)
    _set_paragraph_spacing(p, before_pt=4, after_pt=8, line=1.4)
    _add_run_with_cn_font(p, text, size_pt=11, italic=True, color="404040")
    return p


def add_list_item(doc, text, ordered=False, index=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.74)
    pf.first_line_indent = Cm(-0.74)
    _set_paragraph_spacing(p, after_pt=2, line=1.4)
    bullet = f"{index}." if ordered and index else "•"
    _add_run_with_cn_font(p, f"{bullet} ", size_pt=12)
    _add_run_with_cn_font(p, text, size_pt=12)
    return p


def add_code_block(doc, code_text):
    """Code block: monospace, gray background, no first-line indent."""
    for line in code_text.split("\n"):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.3)
        pf.right_indent = Cm(0.3)
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        _add_shading(p, "F5F5F5")
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(10)
        _set_cn_font(run, "Consolas", "SimSun")
    # trailing spacer
    spacer = doc.add_paragraph()
    _set_paragraph_spacing(spacer, before_pt=0, after_pt=4, line=1.0)


def add_formula(doc, formula_text):
    """LaTeX formula: italic Cambria Math / fallback to italic text in box."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.left_indent = Cm(0.3)
    pf.right_indent = Cm(0.3)
    _set_paragraph_spacing(p, before_pt=8, after_pt=8, line=1.4)
    run = p.add_run(formula_text)
    run.font.name = "Cambria Math"
    run.font.size = Pt(11)
    run.italic = True
    _set_cn_font(run, "Cambria Math", "SimSun")
    return p


def add_image(doc, path, caption_text=None, width_inches=5.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_paragraph_spacing(p, before_pt=8, after_pt=4, line=1.0)
    run = p.add_run()
    if Path(path).exists():
        run.add_picture(str(path), width=Inches(width_inches))
    else:
        # missing image placeholder
        run = p.add_run(f"[图: {Path(path).name} 未找到]")
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        _set_cn_font(run, "Times New Roman", "SimSun")

    if caption_text:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_paragraph_spacing(cp, before_pt=0, after_pt=10, line=1.3)
        _add_run_with_cn_font(cp, caption_text, size_pt=10, italic=True, color="404040")
    return p


def add_three_line_table(doc, headers, rows, caption=None):
    """Academic three-line table: top rule, header-bottom rule, bottom rule only."""
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        _set_paragraph_spacing(cp, before_pt=8, after_pt=4, line=1.3)
        _add_run_with_cn_font(cp, caption, size_pt=10, bold=True)

    n_cols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=n_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Default: remove all borders, then add only top/header-bottom/bottom
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblBorders = OxmlElement("w:tblBorders")
    for name in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{name}")
        b.set(qn("w:val"), "nil")
        tblBorders.append(b)
    # remove existing
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    tblPr.append(tblBorders)

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_paragraph_spacing(p, before_pt=2, after_pt=2, line=1.2)
        _add_run_with_cn_font(p, h, size_pt=10, bold=True)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        # header bottom rule (heavier)
        _set_cell_borders(
            cell,
            top={"sz": 8, "color": "000000"},
            bottom={"sz": 6, "color": "000000"},
        )

    # Data rows
    for r_idx, row in enumerate(rows):
        is_last = r_idx == len(rows) - 1
        for c_idx, val in enumerate(row):
            cell = table.rows[1 + r_idx].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            _set_paragraph_spacing(p, before_pt=2, after_pt=2, line=1.2)
            _add_run_with_cn_font(p, str(val), size_pt=10)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if is_last:
                # bottom rule (heavier, only on last row)
                _set_cell_borders(
                    cell,
                    bottom={"sz": 8, "color": "000000"},
                )
    return table


def add_horizontal_rule(doc):
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before_pt=4, after_pt=4, line=1.0)
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "808080")
    pBdr.append(bottom)
    pPr.append(pBdr)


# ────────────────────────────────────────────────────────────────────
# Markdown parsing — section by section
# ────────────────────────────────────────────────────────────────────

# Match table rows
TABLE_ROW = re.compile(r"^\|(.+)\|$")
TABLE_SEP = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.+)$")
IMAGE = re.compile(r"^!\[(.*?)\]\((.+?)(?:\s+\".*?\")?\)$")
LIST_OL = re.compile(r"^(\d+)\.\s+(.+)$")
LIST_UL = re.compile(r"^[-*]\s+(.+)$")
BLOCKQUOTE = re.compile(r"^>\s?(.*)$")
FENCE = re.compile(r"^```(.*)$")
HR = re.compile(r"^---+$")


def parse_table_row(line):
    """Parse a markdown table row into list of cells."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def looks_like_table_row(line):
    return bool(TABLE_ROW.match(line.strip()))


def render_md_to_doc(doc, md_text):
    """Render markdown text into the doc. We handle a curated subset
    that covers the report's structure: heading, paragraph, blockquote,
    table, image, code fence, formula (LaTeX block), hr, ordered/unordered list.
    """
    lines = md_text.split("\n")
    i = 0
    n = len(lines)

    def blank():
        return i < n and lines[i].strip() == ""

    def peek():
        return lines[i] if i < n else ""

    # state
    in_code = False
    code_buf = []
    code_lang = ""

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ── fenced code ──
        m = FENCE.match(stripped)
        if m:
            if not in_code:
                in_code = True
                code_lang = m.group(1).strip()
                code_buf = []
            else:
                # closing
                add_code_block(doc, "\n".join(code_buf))
                in_code = False
                code_buf = []
                code_lang = ""
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # ── blank line ──
        if not stripped:
            i += 1
            continue

        # ── horizontal rule ──
        if HR.match(stripped):
            add_horizontal_rule(doc)
            i += 1
            continue

        # ── heading ──
        m = HEADING.match(stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            add_heading(doc, text, level)
            i += 1
            continue

        # ── image (alone on line, possibly with caption following as italic, possibly with blank lines in between) ──
        m = IMAGE.match(stripped)
        if m:
            alt = m.group(1)
            target = m.group(2)
            # resolve relative path against MD directory
            img_path = (MD_PATH.parent / target).resolve()
            # look ahead (skipping blank lines) for an italic caption
            caption = alt if alt else None
            j = i + 1
            # skip blank lines
            while j < n and not lines[j].strip():
                j += 1
            if j < n:
                cap_m = re.match(r"^\*(.+)\*\s*$", lines[j].strip())
                if cap_m:
                    caption = cap_m.group(1).strip()
                    i = j  # skip past caption line (next loop iteration will move past it)
            add_image(doc, str(img_path), caption)
            i += 1
            continue

        # ── LaTeX display formula ($$ ... $$ on its own line) ──
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            add_formula(doc, stripped[2:-2].strip())
            i += 1
            continue
        if stripped.startswith("$$"):
            # multi-line formula
            buf = [stripped[2:]]
            i += 1
            while i < n and not lines[i].strip().endswith("$$"):
                buf.append(lines[i])
                i += 1
            if i < n:
                last = lines[i].strip()
                buf.append(last[:-2])
                i += 1
            add_formula(doc, "\n".join(buf))
            continue

        # ── table ──
        if looks_like_table_row(stripped):
            header = parse_table_row(stripped)
            # expect separator on next line
            if i + 1 < n and TABLE_SEP.match(lines[i + 1].strip()):
                i += 2
                rows = []
                while i < n and looks_like_table_row(lines[i].strip()):
                    rows.append(parse_table_row(lines[i]))
                    i += 1
                # column count normalization
                ncols = len(header)
                rows = [r + [""] * (ncols - len(r)) if len(r) < ncols else r[:ncols] for r in rows]
                add_three_line_table(doc, header, rows)
                continue
            else:
                # not a table — treat as paragraph
                add_paragraph(doc, stripped, first_line_indent=False)
                i += 1
                continue

        # ── blockquote ──
        m = BLOCKQUOTE.match(stripped)
        if m:
            qtext = m.group(1).strip()
            # collect continuation lines that also start with '>' or are blank-continuations
            block_lines = [qtext]
            i += 1
            while i < n:
                l = lines[i]
                ls = l.strip()
                if not ls:
                    break
                bm = BLOCKQUOTE.match(ls)
                if bm:
                    block_lines.append(bm.group(1).strip())
                    i += 1
                    continue
                # continued inline (not '>') — break out and let next iteration handle
                break
            add_blockquote(doc, " ".join(block_lines))
            continue

        # ── ordered list ──
        m = LIST_OL.match(stripped)
        if m:
            idx = int(m.group(1))
            text = m.group(2).strip()
            add_list_item(doc, text, ordered=True, index=idx)
            i += 1
            continue

        # ── unordered list ──
        m = LIST_UL.match(stripped)
        if m:
            text = m.group(1).strip()
            add_list_item(doc, text, ordered=False)
            i += 1
            continue

        # ── default paragraph (collapse soft wraps) ──
        para_lines = [stripped]
        i += 1
        while i < n:
            l = lines[i]
            ls = l.strip()
            if not ls:
                break
            # stop on any block-level start
            if (HEADING.match(ls) or TABLE_ROW.match(ls) or IMAGE.match(ls)
                or FENCE.match(ls) or BLOCKQUOTE.match(ls) or HR.match(ls)
                or ls.startswith("$$") or LIST_OL.match(ls) or LIST_UL.match(ls)):
                break
            para_lines.append(ls)
            i += 1
        add_paragraph(doc, " ".join(para_lines))


# ────────────────────────────────────────────────────────────────────
# Special pre-processing of the source MD
# ────────────────────────────────────────────────────────────────────

def preprocess_md(text):
    """Strip blockquote wrapper from abstract; convert references list."""
    # The MD has an abstract inside a blockquote:
    #   > 摘要. ... 关键词：...
    # We want to split it: the first line is the abstract; the second is keywords.
    # Simpler: detect blockquote at start, take first sentence as abstract, rest as paragraph.

    # Title and subtitle are non-block (already plain).
    # The blockquote (line 5) contains the abstract.
    # The **关键词** paragraph (line 7) is the keywords.
    # All good — our parser handles these correctly.

    return text


# ────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────

# Module-level footnote definitions collected during MD parse.
# Maps footnote id (int) -> text (str, with *italic* markers).
_FOOTNOTE_DEFS = {}

# Module-level header text for the page header.
_HEADER_TEXT = "摩洛哥参与型住房融资研究 · 2025年12月"


def _scan_footnote_definitions(lines):
    """Scan all MD lines for [^N]: definition blocks.

    A definition starts with `[^N]:` and continues across lines until a blank
    line or the next `[^M]:` definition. Returns dict {id: text}.
    """
    defs = {}
    current_id = None
    current_buf = []
    for line in lines:
        stripped = line.strip()
        m = re.match(r"^\[\^(\d+)\]:\s*(.*)$", stripped)
        if m:
            # Save previous definition
            if current_id is not None:
                defs[current_id] = " ".join(s for s in current_buf if s).strip()
            current_id = int(m.group(1))
            current_buf = [m.group(2).strip()]
            continue
        if current_id is not None:
            if not stripped:
                # blank line ends the definition
                defs[current_id] = " ".join(s for s in current_buf if s).strip()
                current_id = None
                current_buf = []
            else:
                current_buf.append(stripped)
    # Tail definition
    if current_id is not None:
        defs[current_id] = " ".join(s for s in current_buf if s).strip()
    return defs


def main():
    md_text = MD_PATH.read_text(encoding="utf-8")
    md_text = preprocess_md(md_text)

    doc = setup_document()

    # Title (line 1 — # heading)
    # Subtitle (line 3 — bold)
    # Abstract (line 5 — blockquote starting "摘要.")
    # Keywords (line 7 — bold **关键词**)

    lines = md_text.split("\n")
    # Scan footnote definitions first (so they're available for the post-processor)
    global _FOOTNOTE_DEFS
    _FOOTNOTE_DEFS = _scan_footnote_definitions(lines)
    print(f"Footnote definitions found: {len(_FOOTNOTE_DEFS)} ({sorted(_FOOTNOTE_DEFS.keys())})")

    # extract title from "# ..."
    title = ""
    i0 = 0
    for k, l in enumerate(lines):
        m = HEADING.match(l.strip())
        if m and len(m.group(1)) == 1:
            title = m.group(2).strip()
            i0 = k + 1
            break

    # extract subtitle: first non-empty line after title
    # (must not be a heading, blockquote, or horizontal rule)
    subtitle = ""
    while i0 < len(lines):
        l = lines[i0].strip()
        if not l:
            i0 += 1
            continue
        if l.startswith("#") or l.startswith(">") or l == "---":
            break
        subtitle = l
        # strip surrounding ** if present (handles both fully-bold and partially-bold)
        if subtitle.startswith("**") and subtitle.endswith("**"):
            subtitle = subtitle.strip("*").strip()
        i0 += 1
        break

    # render title and subtitle
    add_title(doc, title)
    add_subtitle(doc, subtitle)

    # Then skip past the blockquote (abstract) and keywords line in the source,
    # because we'll render them specially.
    # Skip "---" separator
    while i0 < len(lines):
        l = lines[i0].strip()
        if not l or l == "---":
            i0 += 1
            continue
        if l.startswith(">"):
            # abstract blockquote
            buf = []
            while i0 < len(lines) and lines[i0].strip().startswith(">"):
                buf.append(lines[i0].strip()[1:].strip())
                i0 += 1
            abstract_text = " ".join(b for b in buf if b)
            # Strip the leading "摘要." or "摘要：" if present in source — we add our own label
            abstract_text = re.sub(r"^摘要\s*[.：:]\s*", "", abstract_text)
            add_abstract(doc, "摘要", abstract_text)
            continue
        if l.startswith("**关键词**"):
            # strip ALL leading asterisks, then strip "关键词**：" or "关键词：**" prefix
            kw = re.sub(r"^\*+关键词\**\s*[：:]\s*", "", l).strip()
            add_keywords(doc, kw)
            i0 += 1
            continue
        # stop special handling
        break

    # Render the rest, skipping the first part we already consumed
    remaining_lines = lines[i0:]

    # Find and drop the footnote-definition tail section (heading + blockquote intro
    # + all `[^N]:` lines) since the footnotes are emitted as Word footnotes at page
    # bottom and don't need an inline list at the end of the document.
    cut_idx = None
    for k, ll in enumerate(remaining_lines):
        s = ll.strip()
        if s.startswith("**参考文献") or re.match(r"^\[\^\d+\]:", s):
            cut_idx = k
            break
    if cut_idx is not None:
        remaining_lines = remaining_lines[:cut_idx]

    remaining = "\n".join(remaining_lines)
    render_md_to_doc(doc, remaining)

    DOCX_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(DOCX_PATH))
    print(f"Saved: {DOCX_PATH}")
    print(f"Size: {DOCX_PATH.stat().st_size} bytes")

    # Inject Word footnotes part (footnotes.xml + styles) so the [N] markers
    # reference real Word footnotes instead of being literal text.
    if _FOOTNOTE_DEFS:
        _inject_word_footnotes(DOCX_PATH, _FOOTNOTE_DEFS)
        print(f"Injected {len(_FOOTNOTE_DEFS)} Word footnotes.")
        print(f"Final size: {DOCX_PATH.stat().st_size} bytes")


# ────────────────────────────────────────────────────────────────────
# Word footnotes injection (post-process the DOCX)
# ────────────────────────────────────────────────────────────────────

import zipfile
import shutil


def _footnote_text_to_runs_xml(text):
    """Convert a footnote text (with *italic* and **bold** markers) to <w:r> XML."""
    text_escaped = (text.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text_escaped)
    out = []
    for part in parts:
        if not part:
            continue
        is_bold = part.startswith("**") and part.endswith("**")
        is_italic = part.startswith("*") and part.endswith("*") and not is_bold
        clean = part.strip("*").strip()
        if not clean:
            continue
        rpr_inner = []
        if is_bold:
            rpr_inner.append("<w:b/><w:bCs/>")
        if is_italic:
            rpr_inner.append("<w:i/><w:iCs/>")
        rpr = f"<w:rPr>{''.join(rpr_inner)}</w:rPr>" if rpr_inner else ""
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{clean}</w:t></w:r>')
    return "".join(out)


def _build_footnote_element(fn_id, text):
    """Build a single <w:footnote w:id="N"> element with the given text."""
    runs_xml = _footnote_text_to_runs_xml(text)
    return (
        f'<w:footnote w:id="{fn_id}">'
        f'<w:p>'
        f'<w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
        # auto-generated reference mark (the [N] number in the page-bottom)
        f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>'
        f'<w:r><w:t xml:space="preserve"> </w:t></w:r>'
        f'{runs_xml}'
        f'</w:p>'
        f'</w:footnote>'
    )


def _ensure_footnote_styles(styles_xml):
    """Ensure FootnoteReference (character) and FootnoteText (paragraph) styles exist."""
    if 'w:styleId="FootnoteReference"' in styles_xml and 'w:styleId="FootnoteText"' in styles_xml:
        return styles_xml  # already there

    insertion = (
        '<w:style w:type="character" w:styleId="FootnoteReference">'
        '<w:name w:val="footnote reference"/>'
        '<w:uiPriority w:val="99"/>'
        '<w:semiHidden/>'
        '<w:unhideWhenUsed/>'
        '<w:rPr><w:vertAlign w:val="superscript"/></w:rPr>'
        '</w:style>'
        '<w:style w:type="paragraph" w:styleId="FootnoteText">'
        '<w:name w:val="footnote text"/>'
        '<w:basedOn w:val="Normal"/>'
        '<w:link w:val="FootnoteTextChar"/>'
        '<w:uiPriority w:val="99"/>'
        '<w:semiHidden/>'
        '<w:unhideWhenUsed/>'
        '<w:pPr><w:spacing w:after="0"/></w:pPr>'
        '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        '</w:style>'
        '<w:style w:type="character" w:styleId="FootnoteTextChar" w:customStyle="1">'
        '<w:name w:val="Footnote Text Char"/>'
        '<w:basedOn w:val="DefaultParagraphFont"/>'
        '<w:link w:val="FootnoteText"/>'
        '<w:uiPriority w:val="99"/>'
        '<w:semiHidden/>'
        '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        '</w:style>'
    )
    return styles_xml.replace("</w:styles>", insertion + "</w:styles>")


def _inject_word_footnotes(docx_path, defs):
    """Post-process the DOCX: add Word footnote content + footnote styles.

    python-docx's default Document().save() does NOT include word/footnotes.xml,
    so we have to add the part from scratch along with the relationship and
    content-type override.
    """
    # Build a minimal but valid footnotes.xml
    fns_body = (
        '<w:footnote w:type="separator" w:id="-1">'
        '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:separator/></w:r></w:p></w:footnote>'
        '<w:footnote w:type="continuationSeparator" w:id="0">'
        '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
    )
    fns_body += "".join(_build_footnote_element(fid, defs[fid])
                          for fid in sorted(defs.keys()))
    footnotes_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:footnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'{fns_body}'
        '</w:footnotes>'
    )

    tmp_path = docx_path.with_suffix(".docx.tmp")
    with zipfile.ZipFile(docx_path, "r") as zin, \
         zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        has_footnotes = "word/footnotes.xml" in zin.namelist()
        has_rels = "word/_rels/document.xml.rels" in zin.namelist()
        has_ct = "[Content_Types].xml" in zin.namelist()

        rels_xml = None
        ct_xml = None
        if has_rels:
            rels_xml = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        if has_ct:
            ct_xml = zin.read("[Content_Types].xml").decode("utf-8")

        # Ensure document.xml.rels has a footnotes relationship
        if rels_xml is not None and 'Target="footnotes.xml"' not in rels_xml:
            # find max rId
            existing_ids = re.findall(r'Id="rId(\d+)"', rels_xml)
            next_id = max((int(x) for x in existing_ids), default=0) + 1
            new_rel = (
                f'<Relationship Id="rId{next_id}" '
                f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" '
                f'Target="footnotes.xml"/>'
            )
            rels_xml = rels_xml.replace("</Relationships>", new_rel + "</Relationships>")

        # Ensure [Content_Types].xml has the footnotes content type
        if ct_xml is not None and 'PartName="/word/footnotes.xml"' not in ct_xml:
            override = (
                '<Override PartName="/word/footnotes.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
            )
            ct_xml = ct_xml.replace("</Types>", override + "</Types>")

        for item in zin.namelist():
            data = zin.read(item)
            if item == "word/styles.xml":
                text = data.decode("utf-8")
                text = _ensure_footnote_styles(text)
                data = text.encode("utf-8")
            elif item == "word/footnotes.xml":
                data = footnotes_xml.encode("utf-8")
            elif item == "word/_rels/document.xml.rels" and rels_xml is not None:
                data = rels_xml.encode("utf-8")
            elif item == "[Content_Types].xml" and ct_xml is not None:
                data = ct_xml.encode("utf-8")
            zout.writestr(item, data)

        # Add the footnotes.xml part if it didn't exist
        if not has_footnotes:
            zout.writestr("word/footnotes.xml", footnotes_xml)

    shutil.move(str(tmp_path), str(docx_path))


if __name__ == "__main__":
    # Allow CLI override: python md_to_docx.py [md_path] [docx_path] [--header "..."]
    args = sys.argv[1:]
    _cli_header = None
    if "--header" in args:
        idx = args.index("--header")
        _cli_header = args[idx + 1]
        del args[idx:idx + 2]
    if _cli_header is not None:
        _HEADER_TEXT = _cli_header
    if len(args) >= 1:
        MD_PATH = Path(args[0])
    if len(args) >= 2:
        DOCX_PATH = Path(args[1])
    main()