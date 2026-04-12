"""
UJ Prospectus PDF Reader
========================
Extracts qualification data from the University of Johannesburg undergraduate
prospectus PDF and outputs structured JSON matching the Univice data model.

Uses pdfplumber's extract_tables() which reliably reads the tabular layout.
Handles reversed (RTL-encoded) text in header and data cells.
"""
import json
import re
from typing import Any, Dict, List, Optional

import pdfplumber

# ── Config ──────────────────────────────────────────────────

INSTITUTION_NAME = "University of Johannesburg"
INSTITUTION_ABBR = "UJ"

# Column indices in the extracted table (0-based)
COL_PROGRAMME = 0
COL_QUAL_CODE = 1
COL_MIN_APS = 2
COL_ENGLISH = 3
COL_MATHEMATICS = 4
COL_MATH_LIT = 5
COL_TECH_MATH = 6
COL_CAREER = 7
COL_CAMPUS = 8


# ── Text helpers ────────────────────────────────────────────

def clean(s: Optional[str]) -> str:
    """Normalise whitespace, strip, collapse."""
    if not s:
        return ""
    s = s.replace("\n", " ").replace("\r", " ")
    s = s.replace("￾", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def reverse_rtl(s: str) -> str:
    """Reverse a string that was encoded right-to-left in the PDF."""
    return s[::-1]


def is_reversed(s: str) -> bool:
    """Heuristic: if the string contains known reversed markers, it's RTL."""
    markers = [
        "edoC", "noitac", "SPA", "muminiM", "hsilgnE",
        "scitamehtaM", "ycaretiL", "lacinhceT", "REERAC",
        "SUPMAC", "EMMARGORP", "detpecca", "htiw",
    ]
    return any(m in s for m in markers)


def decode_cell(raw: Optional[str]) -> str:
    """Decode a single table cell, handling RTL reversal and common fixups."""
    if not raw:
        return ""
    text = clean(raw)
    if not text:
        return ""

    # Check if the whole cell is reversed
    if is_reversed(text):
        # Split by spaces, reverse each token, then reverse token order
        # This handles multi-word reversed cells like "detpecca toN" -> "Not accepted"
        parts = text.split()
        decoded = " ".join(reverse_rtl(p) for p in reversed(parts))
        text = clean(decoded)

    # Decode level/percentage patterns like ")+%06( 5" -> "5 (60%+)"
    text = re.sub(r"\)\+%(\d+)\(\s*(\d+)", r"\2 (\1%+)", text)
    # Also handle already-partially-decoded "(60%+)5" -> "5 (60%+)"
    text = re.sub(r"\((\d+%\+)\)\s*(\d+)", r"\2 (\1%+)", text)

    return clean(text)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def cell(row: List[Optional[str]], idx: int) -> str:
    """Safely get a cell value from a row, returning '' if out of bounds."""
    if idx < len(row):
        return row[idx] or ""
    return ""


# ── Level parsing ───────────────────────────────────────────

def parse_level(cell_text: str) -> Optional[int]:
    """
    Parse a subject level from a cell value.
    "5 (60%+)" -> 5
    "Not accepted" -> None (signals disallowed)
    "" -> None
    """
    text = decode_cell(cell_text)
    if not text:
        return None
    if "not accepted" in text.lower():
        return None
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else None


def is_not_accepted(cell_text: str) -> bool:
    """Check if a cell explicitly says 'Not accepted'."""
    text = decode_cell(cell_text)
    return "not accepted" in text.lower()


# ── APS parsing ─────────────────────────────────────────────

def parse_aps_cell(raw_aps: str, row: List[Optional[str]]) -> Dict[str, Any]:
    """
    Parse the Minimum APS cell which can be:
    - A plain number: "28"
    - A conditional string (reversed): "25 with Maths OR 26 with Mathematical Literacy"
    Returns { minimum_aps: int, aps_rules: [...] }
    """
    text = decode_cell(raw_aps)
    if not text:
        return {"minimum_aps": None, "aps_rules": []}

    # Plain number
    if re.fullmatch(r"\d+", text):
        return {
            "minimum_aps": int(text),
            "aps_rules": [],
        }

    # Parse conditional APS patterns
    conditions = []
    math_level = parse_level(cell(row, COL_MATHEMATICS))
    math_lit_level = parse_level(cell(row, COL_MATH_LIT))
    tech_math_level = parse_level(cell(row, COL_TECH_MATH))

    # Pattern: "25 with Maths/Tech Maths OR 26 with Mathematical Literacy"
    # or: "25 with Mathematics OR 26 with Mathematical Literacy"
    m = re.search(r"(\d+)\s+with\s+.+?OR\s+(\d+)\s+with\s+.+Literacy", text, re.IGNORECASE)
    if m:
        aps_math = int(m.group(1))
        aps_lit = int(m.group(2))

        if math_level is not None:
            conditions.append({
                "subject": "Mathematics",
                "minimum_level": math_level,
                "min_aps": aps_math,
            })
        if tech_math_level is not None and "Tech" in text:
            conditions.append({
                "subject": "Technical Mathematics",
                "minimum_level": tech_math_level,
                "min_aps": aps_math,
            })
        if math_lit_level is not None:
            conditions.append({
                "subject": "Mathematical Literacy",
                "minimum_level": math_lit_level,
                "min_aps": aps_lit,
            })

        min_aps = min(aps_math, aps_lit)
        return {
            "minimum_aps": min_aps,
            "aps_rules": [{
                "type": "subject_dependent_minimum_aps",
                "conditions": conditions,
            }] if conditions else [],
        }

    # Fallback: try to extract any number
    nums = re.findall(r"\d+", text)
    if nums:
        return {
            "minimum_aps": min(int(n) for n in nums),
            "aps_rules": [],
        }

    return {"minimum_aps": None, "aps_rules": []}


# ── Subject requirements ────────────────────────────────────

def build_subject_requirements(row: List[Optional[str]]) -> Dict[str, List]:
    """Build the grouped subject requirements from a table row."""
    mandatory = []
    one_of = []
    disallowed = []

    # English — always mandatory if present
    eng_level = parse_level(cell(row, COL_ENGLISH))
    if eng_level is not None:
        mandatory.append({"subject": "English", "minimum_level": eng_level})

    # Mathematics
    math_level = parse_level(cell(row, COL_MATHEMATICS))
    math_not_accepted = is_not_accepted(cell(row, COL_MATHEMATICS))

    # Mathematical Literacy
    lit_level = parse_level(cell(row, COL_MATH_LIT))
    lit_not_accepted = is_not_accepted(cell(row, COL_MATH_LIT))

    # Technical Mathematics
    tech_level = parse_level(cell(row, COL_TECH_MATH))
    tech_not_accepted = is_not_accepted(cell(row, COL_TECH_MATH))

    # Determine math subject grouping
    if math_level is not None and lit_level is not None:
        # Both accepted -> one_of (alternatives)
        one_of.append({"subject": "Mathematics", "minimum_level": math_level})
        one_of.append({"subject": "Mathematical Literacy", "minimum_level": lit_level})
    elif math_level is not None and lit_not_accepted:
        # Only pure maths, lit disallowed
        mandatory.append({"subject": "Mathematics", "minimum_level": math_level})
        disallowed.append({"subject": "Mathematical Literacy", "minimum_level": 0})
    elif math_level is not None:
        one_of.append({"subject": "Mathematics", "minimum_level": math_level})
    elif lit_level is not None:
        one_of.append({"subject": "Mathematical Literacy", "minimum_level": lit_level})

    # Technical Mathematics
    if tech_not_accepted:
        disallowed.append({"subject": "Technical Mathematics", "minimum_level": 0})
    elif tech_level is not None:
        one_of.append({"subject": "Technical Mathematics", "minimum_level": tech_level})

    # If maths is disallowed
    if math_not_accepted:
        disallowed.append({"subject": "Mathematics", "minimum_level": 0})

    return {"mandatory": mandatory, "one_of": one_of, "disallowed": disallowed}


# ── Programme name normalisation ────────────────────────────

def normalize_programme_name(raw: str) -> str:
    """
    BA (COMMUNICATION DESIGN) -> BA Communication Design
    ACCOUNTING -> Accounting
    PUBLIC MANAGEMENT AND GOVERNANCE -> Public Management And Governance
    """
    text = clean(raw).replace("✪", "").strip()
    m = re.match(r"^([A-Z]+)\s*\((.+)\)$", text)
    if m:
        prefix = m.group(1).strip()
        inner = m.group(2).strip().title()
        return f"{prefix} {inner}"
    return text.title()


# ── Section heading detection ───────────────────────────────

def parse_section_heading(text: str) -> Optional[Dict[str, str]]:
    """
    Detect rows like "Bachelor of Commerce Degree (3 years)" or
    "BA Degree (3 years)" which are section headers, not qualifications.
    """
    text = clean(text)
    m = re.match(
        r"^((?:Bachelor\s+(?:of\s+\w+\s+)?|B\w+\s+)(?:Extended\s+)?Degree)\s*\((\d+\s*years?)\)$",
        text,
        re.IGNORECASE,
    )
    if m:
        return {
            "qualification_type": clean(m.group(1)),
            "duration": clean(m.group(2)),
        }
    # Also match "DEGREE PROGRAMMES" header
    if re.match(r"^DEGREE PROGRAMMES$", text, re.IGNORECASE):
        return {"qualification_type": None, "duration": None}
    return None


# ── Row classification ──────────────────────────────────────

def is_qualification_row(row: List[Optional[str]]) -> bool:
    """A row is a qualification if it has a programme name and a qualification code."""
    return bool(cell(row, COL_PROGRAMME)) and bool(cell(row, COL_QUAL_CODE))


# ── Page parser ─────────────────────────────────────────────

def parse_page(page, default_faculty: Optional[str] = None) -> List[Dict[str, Any]]:
    """Parse a single PDF page and return a list of qualification dicts."""
    tables = page.extract_tables()
    if not tables:
        return []

    qualifications = []
    current_section = {"qualification_type": None, "duration": None}

    for table in tables:
        for row in table:
            if not row or len(row) < 2 or not row[COL_PROGRAMME]:
                continue

            programme_text = clean(row[COL_PROGRAMME])

            # Skip header rows
            if programme_text in ("EMMARGORP", "PROGRAMME", ""):
                continue

            # Check for section heading
            heading = parse_section_heading(programme_text)
            if heading is not None:
                current_section = heading
                continue

            # Must be a qualification row
            if not is_qualification_row(row):
                continue

            name = normalize_programme_name(programme_text)
            qual_code = clean(cell(row, COL_QUAL_CODE)).replace(" ", "")

            # Skip junk rows (single chars, reversed headers, etc.)
            if len(name) <= 2 or len(qual_code) <= 2:
                continue
            # Skip rows where the name still contains reversed text markers
            if "noitac" in name.lower() or "emmargorp" in name.lower():
                continue

            career_text = clean(cell(row, COL_CAREER))
            campus = clean(cell(row, COL_CAMPUS))

            aps_data = parse_aps_cell(cell(row, COL_MIN_APS), row)
            subject_reqs = build_subject_requirements(row)

            qualifications.append({
                "id": f"{INSTITUTION_ABBR.lower()}-{slugify(name)}",
                "name": name,
                "qualification_code": qual_code,
                "faculty": default_faculty,
                "qualification_type": current_section.get("qualification_type"),
                "duration": current_section.get("duration"),
                "description": career_text,
                "campus": campus,
                "minimum_aps": aps_data["minimum_aps"],
                "aps_rules": aps_data["aps_rules"],
                "subject_requirements": subject_reqs,
                "selection_requirements": [],
            })

    return qualifications


# ── Validation ──────────────────────────────────────────────

def validate_qualification(q: Dict[str, Any]) -> List[str]:
    """Return a list of warning messages for a qualification."""
    warnings = []
    if not q.get("qualification_code"):
        warnings.append(f"Missing qualification_code for {q.get('name')}")
    if not q.get("name"):
        warnings.append(f"Missing name for {q.get('qualification_code')}")
    if q.get("minimum_aps") is None:
        warnings.append(f"Missing minimum_aps for {q.get('name')}")
    if not q.get("subject_requirements", {}).get("mandatory"):
        warnings.append(f"No mandatory subjects for {q.get('name')}")
    return warnings


# ── Full PDF parser ─────────────────────────────────────────

def parse_uj_pdf(
    pdf_path: str,
    output_path: Optional[str] = None,
    default_faculty: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Parse the entire UJ prospectus PDF and return structured JSON.
    Deduplicates by qualification_code.
    """
    all_qualifications = []
    page_reports = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for page_num, page in enumerate(pdf.pages):
            try:
                quals = parse_page(page, default_faculty=default_faculty)
                all_qualifications.extend(quals)
                page_reports.append({
                    "page": page_num,
                    "status": "ok",
                    "count": len(quals),
                })
            except Exception as e:
                page_reports.append({
                    "page": page_num,
                    "status": "error",
                    "error": str(e),
                })

    # Deduplicate by qualification_code
    seen = {}
    for q in all_qualifications:
        code = q.get("qualification_code")
        if code and code not in seen:
            seen[code] = q

    deduped = list(seen.values())

    # Validate
    all_warnings = []
    for q in deduped:
        all_warnings.extend(validate_qualification(q))

    result = {
        "name": INSTITUTION_NAME,
        "abbr": INSTITUTION_ABBR,
        "qualifications": deduped,
        "meta": {
            "total_qualifications": len(deduped),
            "pages_processed": total_pages,
            "warnings": all_warnings,
            "page_reports": page_reports,
        },
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ── Single page convenience ─────────────────────────────────

def parse_uj_pdf_page(
    pdf_path: str,
    page_number: int = 0,
    output_path: Optional[str] = None,
    default_faculty: Optional[str] = None,
) -> Dict[str, Any]:
    """Parse a single page and return structured JSON."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        quals = parse_page(page, default_faculty=default_faculty)

    result = {
        "name": INSTITUTION_NAME,
        "abbr": INSTITUTION_ABBR,
        "qualifications": quals,
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "uj-tables.pdf"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "uj_univice_all_pages.json"

    result = parse_uj_pdf(pdf_path=pdf_path, output_path=output_path)

    print(f"Extracted {result['meta']['total_qualifications']} qualifications "
          f"from {result['meta']['pages_processed']} pages")

    if result["meta"]["warnings"]:
        print(f"\nWarnings ({len(result['meta']['warnings'])}):")
        for w in result["meta"]["warnings"]:
            print(f"  - {w}")
