import fitz  # PyMuPDF
import re

def extract_sections(pdf_path):
    """
    Extract headings (H1, H2, H3) with page numbers and capture 
    all text contained under each heading until the next heading.
    
    Returns:
        List of dicts with keys:
          - 'level': "H1", "H2", or "H3"
          - 'title': heading text
          - 'page': page number (int)
          - 'text': full text content under the heading
    """
    doc = fitz.open(pdf_path)
    blocks_info = []

    # Step 1: Extract spans with text and font size info
    for page_no in range(len(doc)):
        page = doc[page_no]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    blocks_info.append({
                        "text": text,
                        "size": round(span["size"]),
                        "flags": span["flags"],
                        "page": page_no + 1,
                        "block_order": len(blocks_info),
                    })

    if not blocks_info:
        return []

    # Step 2: Determine font sizes for headings
    font_sizes = sorted({b["size"] for b in blocks_info}, reverse=True)
    # Use top 3 font sizes for H1, H2, H3
    heading_font_sizes = font_sizes[:3] if len(font_sizes) >= 3 else font_sizes

    size_to_level = {}
    for i, sz in enumerate(heading_font_sizes):
        size_to_level[sz] = f"H{i+1}"

    # Step 3: Identify headings
    headings = []
    for idx, b in enumerate(blocks_info):
        sz = b["size"]
        if sz in size_to_level:
            # Heuristic filters to avoid false headings (e.g., too long lines, page numbers)
            text = b["text"]
            if 3 <= len(text) <= 120 and not re.match(r"^[\d.\s-]+$", text):
                headings.append({
                    "index": idx,
                    "level": size_to_level[sz],
                    "title": text,
                    "page": b["page"],
                })

    # Step 4: Extract text under each heading until next heading
    sections = []
    for i, head in enumerate(headings):
        start_idx = head["index"] + 1
        end_idx = headings[i+1]["index"] if i+1 < len(headings) else len(blocks_info)

        # Collect all text spans between this heading and the next
        section_texts = []
        for j in range(start_idx, end_idx):
            # Avoid headings inside, only text blocks
            if j < len(blocks_info):
                section_texts.append(blocks_info[j]["text"])
        full_text = " ".join(section_texts).strip()

        sections.append({
            "level": head["level"],
            "title": head["title"],
            "page": head["page"],
            "text": full_text
        })

    return sections
