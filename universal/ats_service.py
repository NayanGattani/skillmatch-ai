"""Deterministic ATS-readiness checks; never presented as ATS pass probability."""
from __future__ import annotations
from typing import Any

def _check(key,label,passed,weight,detail): return {"key":key,"label":label,"passed":passed,"weight":weight,"detail":detail}

def calculate_ats_readiness(d:dict[str,Any])->dict[str,Any]:
    checks=[
      _check("text_extractable","Machine-readable text",d["text_extractable"],25,"Enough selectable text was extracted for automated parsing." if d["text_extractable"] else "Very little text was extracted; this may indicate an image/scanned resume."),
      _check("section_detectability","Detectable resume sections",d["standard_section_count"]>=2,12,f"Detected {d['standard_section_count']} recognizable section headings."),
      _check("contact_detectability","Contact details detectable",d["email_detected"] and d["phone_detected"],8,"Email and phone were detected." if d["email_detected"] and d["phone_detected"] else "One or more common contact fields were not detected."),
      _check("extraction_integrity","Extraction integrity",d["replacement_character_count"]==0 and d["control_character_count"]==0,15,"No obvious replacement/control-character corruption was detected." if d["replacement_character_count"]==0 and d["control_character_count"]==0 else "Extracted text contains corruption-like characters."),
      _check("column_risk","Single-flow layout",not d["likely_two_column"],15,"No strong multi-column extraction risk was detected." if not d["likely_two_column"] else "Multiple columns were detected; reading order can vary across parsers."),
      _check("table_risk","Low table complexity",d["tables"]==0,10,"No tables were detected." if d["tables"]==0 else f"Detected {d['tables']} table-like structure(s)."),
      _check("header_footer_risk","Low repeated header/footer risk",not d["header_footer_signal"],5,"No repeated page-edge text was detected." if not d["header_footer_signal"] else "Repeated page-edge text was detected."),
      _check("text_density","Healthy text extraction density",d["word_count"]>=150 or d.get("words_per_page", d["word_count"]/max(d.get("page_count",1),1)) >= 60,5,"The extracted text volume is plausible for parser-based analysis." if d.get("words_per_page", d["word_count"]/max(d.get("page_count",1),1)) >= 60 else "The extracted text volume is unusually low for a resume page."),
      _check("image_only","No image-only pages",d["image_only_pages"]==0,5,"No page appears to be primarily an image." if d["image_only_pages"]==0 else f"{d['image_only_pages']} page(s) appear primarily image-based."),
    ]
    raw=sum(c["weight"] for c in checks if c["passed"])
    score=max(0,min(100,round(raw,2)))
    warnings=[]
    if not d["text_extractable"]: warnings.append("Very little machine-readable text was extracted.")
    if d["likely_two_column"]: warnings.append("Multi-column layout may produce inconsistent extraction order.")
    if d["tables"]: warnings.append("Table-like structures may reduce parser reliability.")
    if d["header_footer_signal"]: warnings.append("Repeated header/footer content may be parsed inconsistently.")
    if d["image_only_pages"]: warnings.append(f"{d['image_only_pages']} page(s) appear image-based.")
    if d["replacement_character_count"]: warnings.append("Replacement characters suggest extraction corruption.")
    status="strong" if score>=85 else "good" if score>=70 else "needs_attention" if score>=50 else "high_risk"
    return {"score":score,"status":status,"checks":checks,"warnings":warnings,"method":"deterministic parser-oriented checks; not a probability of passing a specific ATS","penalties":{"image_only_pages":0}}
