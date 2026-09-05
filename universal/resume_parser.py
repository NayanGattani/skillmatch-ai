"""Deterministic, occupation-agnostic resume document parser and signals."""
from __future__ import annotations
import re
from collections import Counter
from typing import Any
import pdfplumber

EMAIL_RE=re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",re.I)
PHONE_RE=re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
URL_RE=re.compile(r"\b(?:https?://|www\.)[^\s<>]+",re.I)
BARE_PROFILE_URL_RE=re.compile(r"(?<![@\w])(?:linkedin\.com/(?:in|pub)/[^\s<>]+|github\.com/[^\s<>]+|behance\.net/[^\s<>]+|dribbble\.com/[^\s<>]+|orcid\.org/[^\s<>]+|scholar\.google\.com/[^\s<>]+|kaggle\.com/[^\s<>]+)",re.I)
DATE_RE=re.compile(r"\b(?:19|20)\d{2}\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(?:19|20)\d{2}\b",re.I)
YEAR_RANGE_RE=re.compile(r"\b(?:19|20)\d{2}\s*(?:-|–|—|to)\s*(?:present|current|(?:19|20)\d{2})\b",re.I)
BULLET_RE=re.compile(r"^\s*(?:[-*•▪◦‣–—]|\d+[.)]|[a-z][.)])\s+")

SECTION_ALIASES={
"summary":{"summary","professional summary","profile","professional profile","objective","career objective","about me","overview"},
"experience":{"experience","work experience","professional experience","employment","employment history","work history","career history","professional history","internships","internship","placements"},
"education":{"education","academic background","academic qualifications","qualifications","education & training"},
"skills":{"skills","technical skills","core skills","core competencies","competencies","areas of expertise","expertise","technologies","tools"},
"projects":{"projects","personal projects","academic projects","selected projects","key projects","portfolio","selected work"},
"certifications":{"certifications","certificates","licenses","licenses & certifications","credentials","professional certifications"},
"achievements":{"achievements","awards","honors","accomplishments","distinctions"},
"research":{"research","research experience","publications","research & publications","clinical research"},
"leadership":{"leadership","leadership experience","volunteer experience","community involvement","extracurriculars","activities"},
"languages":{"languages","language skills","languages spoken"},
}
NORM_SECTION={re.sub(r"[^a-z0-9& ]+","",alias.lower()).strip():canon for canon,aliases in SECTION_ALIASES.items() for alias in aliases}

def _clean(line:str)->str: return re.sub(r"\s+"," ",line.replace("\u00a0"," ")).strip()
def _heading_key(line:str)->str: return re.sub(r"[^a-z0-9& ]+","",_clean(line).lower()).strip()

def detect_sections(text:str)->dict[str,Any]:
    lines=[_clean(x) for x in text.splitlines()]
    detected={}
    for i,line in enumerate(lines):
        if not line or len(line)>70: continue
        key=_heading_key(line)
        canon=NORM_SECTION.get(key)
        # Uppercase short headings are accepted only when they resemble a heading;
        # arbitrary all-caps body lines are not promoted to sections.
        if canon is None and line.isupper() and 1<=len(line.split())<=5:
            canon=NORM_SECTION.get(_heading_key(line.title()))
        if canon and canon not in detected: detected[canon]={"heading":line,"line":i+1}
    return {"detected":detected,"count":len(detected),"standard_count":len(detected)}

def _repeated_edge_lines(page_texts):
    if len(page_texts)<2:return []
    c=Counter()
    for text in page_texts:
        lines=[_clean(x) for x in text.splitlines() if _clean(x)]
        for line in lines[:4]+lines[-4:]:
            if len(line)>=5:c[line.lower()]+=1
    return sorted(x for x,n in c.items() if n>=2)

def _column_signal(page):
    try: words=page.extract_words(use_text_flow=False,keep_blank_chars=False)
    except Exception:return {"likely_two_column":False,"confidence":0.0,"reason":"word_positions_unavailable"}
    if len(words)<40:return {"likely_two_column":False,"confidence":0.0,"reason":"insufficient_words"}
    mid=float(page.width)/2
    left=sum(1 for w in words if float(w.get("x0",0))<mid-25)
    right=sum(1 for w in words if float(w.get("x0",0))>mid+25)
    if not left or not right:return {"likely_two_column":False,"confidence":0.0,"reason":"no_separated_words"}
    balance=min(left,right)/max(left,right)
    # Require both substantial volume and balance; this reduces false positives on
    # resumes with a narrow sidebar/contact block.
    likely=left>=18 and right>=18 and balance>=0.50
    confidence=round(min(1.0,balance*1.2),2)
    return {"likely_two_column":likely,"confidence":confidence if likely else round(confidence*0.45,2),"left_words":left,"right_words":right}

def _infer_career_stage(text:str,sections:dict[str,Any],word_count:int)->str:
    lower=text.lower()
    exp=sections["detected"].get("experience")
    project=sections["detected"].get("projects")
    internship=bool(re.search(r"\bintern(?:ship|ed)?\b",lower))
    if exp and (len(re.findall(r"\b(?:19|20)\d{2}\b",text))>=4 or re.search(r"\b(?:senior|lead|manager|director|head|principal|chief)\b",lower)): return "experienced"
    if internship or project: return "student_or_entry_level"
    if not exp and word_count<900:return "student_or_entry_level"
    return "unknown"

def _normalize_url(url:str)->str:
    url=url.strip().strip("<>()[]{}\".,;:!?\u201d\u2019")
    if not url.lower().startswith(("http://", "https://")):
        url="https://"+url
    return url

def _classify_url(url:str)->str:
    lower=url.lower()
    if "linkedin.com" in lower: return "linkedin"
    if "github.com" in lower: return "github"
    if "behance.net" in lower: return "behance"
    if "dribbble.com" in lower: return "dribbble"
    if "orcid.org" in lower: return "orcid"
    if "scholar.google.com" in lower: return "google_scholar"
    if "kaggle.com" in lower: return "kaggle"
    return "other"

def _extract_pdf_links(pdf, extracted_text: str) -> list[dict[str, str]]:
    found = []

    for page_number, page in enumerate(pdf.pages, 1):
        try:
            annotations = page.hyperlinks or []
        except Exception:
            annotations = []

        for annotation in annotations:
            uri = annotation.get("uri") if isinstance(annotation, dict) else None

            if isinstance(uri, str) and uri.strip():
                normalized = _normalize_url(uri)
                link_type = _classify_url(normalized)

                # Ignore non-profile embedded links such as mailto links.
                if link_type == "other":
                    continue

                # Ignore incomplete LinkedIn profile links.
                if link_type == "linkedin" and not re.search(
                    r"linkedin\.com/(?:in|pub)/[^/\s]+",
                    normalized,
                    re.I,
                ):
                    continue

                # Ignore incomplete GitHub profile links.
                if link_type == "github" and not re.search(
                    r"github\.com/[^/\s]+",
                    normalized,
                    re.I,
                ):
                    continue

                found.append(
                    {
                        "url": normalized,
                        "type": link_type,
                        "source": "embedded_link",
                        "page": str(page_number),
                    }
                )

    for raw in URL_RE.findall(extracted_text) + BARE_PROFILE_URL_RE.findall(
        extracted_text
    ):
        url = _normalize_url(raw)

        found.append(
            {
                "url": url,
                "type": _classify_url(url),
                "source": "visible_text",
                "page": "",
            }
        )

    dedup = []
    seen = set()

    for item in found:
        key = item["url"].lower().rstrip("/")

        if key not in seen:
            seen.add(key)
            dedup.append(item)

    return dedup
def analyze_pdf(path:str,text:str|None=None)->dict[str,Any]:
    with pdfplumber.open(path) as pdf:
        page_texts=[]; metrics=[]; total_images=total_tables=0; cols=[]
        for page in pdf.pages:
            ptext=page.extract_text() or ""; page_texts.append(ptext)
            try: words=page.extract_words(use_text_flow=False,keep_blank_chars=False)
            except Exception: words=[]
            images=len(getattr(page,"images",[]) or []); total_images+=images
            try: tables=len(page.find_tables())
            except Exception: tables=0
            total_tables+=tables; cols.append(_column_signal(page))
            metrics.append({"characters":len(ptext),"words":len(words),"images":images,"tables":tables})
        extracted="\n".join(page_texts).strip()
        if text is not None: extracted=text.strip()
        words=re.findall(r"\b\w+(?:['’-]\w+)*\b",extracted,re.UNICODE)
        lines=[_clean(x) for x in extracted.splitlines() if _clean(x)]
        bullets=[x for x in lines if BULLET_RE.match(x)]
        sections=detect_sections(extracted)
        links=_extract_pdf_links(pdf, extracted)
        linkedin=any(x["type"]=="linkedin" for x in links)
        github=any(x["type"]=="github" for x in links)
        portfolio=any(x["type"] in {"behance","dribbble"} or "portfolio" in x["url"].lower() for x in links)
        image_only=sum(1 for m in metrics if m["characters"]<30 and m["images"]>0)
        replacement=extracted.count("�")
        controls=sum(1 for c in extracted if ord(c)<32 and c not in "\n\t\r")
        avg=len(extracted)/max(len(metrics),1)
        # Use words-per-page as a parser-health signal; a ratio of unique characters
        # is not meaningful for resume quality and can penalize legitimate documents.
        words_per_page=len(words)/max(len(metrics),1)
        text_density=round(min(1.0, words_per_page/150),3)
        return {
          "page_count":len(metrics),"word_count":len(words),"character_count":len(extracted),"line_count":len(lines),"bullet_count":len(bullets),
          "bullet_ratio":round(len(bullets)/max(len(lines),1),3),"email_detected":bool(EMAIL_RE.search(extracted)),"phone_detected":bool(PHONE_RE.search(extracted)),
          "linkedin_detected":linkedin,"github_detected":github,"portfolio_detected":portfolio,"url_count":len(links),"links":links,
          "date_count":len(DATE_RE.findall(extracted)),"date_range_count":len(YEAR_RANGE_RE.findall(extracted)),"sections":sections,
          "section_names":sorted(sections["detected"]),"standard_section_count":sections["standard_count"],"images":total_images,"tables":total_tables,
          "likely_two_column":any(x.get("likely_two_column") for x in cols),"column_confidence":max((x.get("confidence",0) for x in cols),default=0),
          "repeated_header_footer_lines":_repeated_edge_lines(page_texts),"header_footer_signal":bool(_repeated_edge_lines(page_texts)),"image_only_pages":image_only,
          "avg_characters_per_page":round(avg,1),"replacement_character_count":replacement,"control_character_count":controls,"text_extractable":len(words)>=20,
          "text_density":text_density,"words_per_page":round(words_per_page,1),"career_stage":_infer_career_stage(extracted,sections,len(words)),"page_metrics":metrics,"text":extracted,"parse_warnings":[],
        }
