"""Universal, explainable resume-to-job matching.

The matcher is intentionally not a CS keyword checker. It combines a broad competency
vocabulary with job-specific phrases extracted from the JD, then evaluates where and
how each requirement is evidenced in the resume. It never invents experience or years.
"""
from __future__ import annotations
import re
from collections import Counter
from typing import Any
from skills import ALL_SKILLS, SKILL_ALIASES, aliases_for, normalize_skill

TOKEN_RE = re.compile(r"[a-z][a-z0-9+#&./'-]*", re.I)
STOPWORDS = set("a an and are as at be been being by can could did do does for from had has have how i if in into is it its may might more must of on or our should than that the their them there these they this to under using was we were what when where which who will with would you your".split())
GENERIC_REQUIREMENT_WORDS = set("ability knowledge experience skills skill understanding proficiency familiar familiarity demonstrated strong excellent good preferred required responsibility responsibilities qualification qualifications role candidate team work working".split())


def _pattern(phrase: str) -> re.Pattern[str]:
    tokens = re.findall(r"[a-z0-9+#&./-]+", phrase.lower())
    if not tokens:
        return re.compile(r"a^", re.I)
    return re.compile(r"(?<!\w)" + r"\s+".join(re.escape(t) for t in tokens) + r"(?!\w)", re.I)


# One compiled alternation is substantially faster than scanning the entire resume
# once for every competency. Alternatives are longest-first so "content strategy"
# wins over the shorter "strategy" at the same location.
_SKILL_CANDIDATES = sorted(set(ALL_SKILLS) | set(SKILL_ALIASES), key=lambda x: (-len(re.findall(r"[a-z0-9+#&./-]+", x)), -len(x)))
_SKILL_CANONICAL_BY_KEY = {re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+#&./-]+", " ", c.lower())).strip(): normalize_skill(c) for c in _SKILL_CANDIDATES}
_SKILL_ALT = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(c) for c in _SKILL_CANDIDATES) + r")(?!\w)", re.I)


def extract_skills(text: str) -> list[str]:
    if not text:
        return []
    found: dict[str, str] = {}
    for match in _SKILL_ALT.finditer(text):
        key = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+#&./-]+", " ", match.group(0).lower())).strip()
        canonical = _SKILL_CANONICAL_BY_KEY.get(key, normalize_skill(match.group(0)))
        found[canonical.lower()] = canonical
    return sorted(found.values(), key=str.lower)


def _canonical_term_set(text: str) -> set[str]:
    return {normalize_skill(x).lower() for x in extract_skills(text)}


def _split_resume_sections(text: str) -> dict[str, list[str]]:
    """Map arbitrary resume headings to generic evidence buckets."""
    aliases = {
      "experience": {"experience","work experience","professional experience","employment","employment history","work history","career history","professional history","internships","internship","placements"},
      "projects": {"projects","selected projects","academic projects","personal projects","key projects","portfolio"},
      "summary": {"summary","professional summary","profile","professional profile","objective","career objective","about me","overview"},
      "skills": {"skills","technical skills","core skills","core competencies","competencies","areas of expertise","expertise","technologies","tools"},
      "education": {"education","academic background","academic qualifications","qualifications","education & training"},
      "certifications": {"certifications","certificates","licenses","licenses & certifications","credentials"},
      "research": {"research","research experience","publications","research & publications","clinical research"},
      "leadership": {"leadership","leadership experience","volunteer experience","community involvement","extracurriculars"},
      "achievements": {"achievements","awards","honors","accomplishments","distinctions"},
      "languages": {"languages","language skills","languages spoken","language proficiency"},
      "volunteering": {"volunteering","volunteer work","community service"},
      "publications": {"publications","selected publications","papers"},
    }
    norm = {re.sub(r"[^a-z0-9& ]+","",k.lower()).strip(): v for v,s in aliases.items() for k in s}
    buckets = {k: [] for k in aliases}; buckets["other"]=[]; current="other"
    for raw in text.splitlines():
        line = re.sub(r"\s+"," ",raw).strip()
        if not line: continue
        key = re.sub(r"[^a-z0-9& ]+","",line.lower()).strip()
        if key in norm:
            current=norm[key]; continue
        buckets[current].append(line)
    return buckets


def extract_skill_evidence(resume_text: str, skills: list[str]) -> dict[str, dict[str, Any]]:
    sections = _split_resume_sections(resume_text)
    result={}
    for skill in skills:
        aliases = aliases_for(skill)
        pats=[_pattern(a) for a in aliases]
        locations=[]
        for section, lines in sections.items():
            if section == "other": continue
            if any(p.search(line) for p in pats for line in lines): locations.append(section)
        if "experience" in locations or "projects" in locations or "research" in locations or "publications" in locations:
            level="strong"
        elif any(x in locations for x in ("summary","certifications","education","leadership","achievements","volunteering")):
            level="moderate"
        elif "skills" in locations:
            level="listed"
        else: level="weak"
        result[skill]={"locations":locations,"evidence_level":level}
    return result

_REQUIRED_HEADER_RE = re.compile(r"^(?:requirements?|required (?:skills?|qualifications?)|must[- ]have|mandatory|essential(?: skills?)?|minimum qualifications?|basic qualifications?|key qualifications?|what you(?:'|’)ll need|you have)",re.I)
_PREFERRED_HEADER_RE = re.compile(r"^(?:preferred(?: skills?| qualifications?)?|nice[- ]to[- ]have|would be a plus|good to have|bonus|optional|desired|ideal(?: qualifications?)?)",re.I)
_REQUIRED_CUE = re.compile(r"\b(?:must|required|essential|mandatory|minimum|need to|you (?:must|should) have|years? of experience|proficien(?:t|cy)|expertise in)\b",re.I)
_PREFERRED_CUE = re.compile(r"\b(?:preferred|nice[- ]to[- ]have|plus|bonus|advantage|desired|ideally|would be great|would be a plus)\b",re.I)
_NEGATED_CUE = re.compile(r"\b(?:not|required not|isn't|is not|aren't|are not)\s+(?:required|mandatory|essential)\b",re.I)


def parse_job_sections(job_description: str) -> dict[str, str]:
    if not job_description or not job_description.strip(): return {"required":"","preferred":""}
    # Normalize inline section markers (common in pasted job descriptions) into
    # line boundaries before applying the section state machine.
    job_description = re.sub(r"\s+(?=(?:Preferred(?: skills?| qualifications?)?|Nice[- ]to[- ]have|Would be (?:great|a plus)|Good to have|Bonus|Optional|Desired|Ideal(?: qualifications?)?)\s*:)", "\n", job_description, flags=re.I)
    job_description = re.sub(r"\s+(?=(?:Requirements?|Required(?: skills?| qualifications?)?|Must[- ]have|Must have|Mandatory|Minimum qualifications?|Basic qualifications?|Key qualifications?)\s*:)", "\n", job_description, flags=re.I)
    required=[]; preferred=[]; current=None; explicit=False
    header=re.compile(r"^(requirements?|required(?: skills?| qualifications?)?|must[- ]have|must have|mandatory|minimum qualifications?|basic qualifications?|key qualifications?|what you(?:'|’)ll need|preferred(?: skills?| qualifications?)?|nice[- ]to[- ]have|would be (?:great|a plus)|good to have|bonus|optional|desired|ideal(?: qualifications?)?)\s*:?-?\s*(.*)$",re.I)
    for raw in job_description.splitlines():
        line=raw.strip()
        if not line: continue
        m=header.match(line)
        if m:
            explicit=True; label=m.group(1).lower(); current="preferred" if re.search(r"preferred|nice|would be|good to have|bonus|optional|desired|ideal",label,re.I) else "required"
            if m.group(2).strip(): (preferred if current=="preferred" else required).append(m.group(2).strip())
            continue
        if current=="required": required.append(line)
        elif current=="preferred": preferred.append(line)
    if explicit: return {"required":" ".join(required),"preferred":" ".join(preferred)}
    for sentence in re.split(r"(?<=[.!?])\s+|\n+",job_description):
        sentence=sentence.strip(" -•\t")
        if not sentence: continue
        # A sentence saying a skill is explicitly not required should not become a requirement.
        if _NEGATED_CUE.search(sentence): continue
        if _PREFERRED_CUE.search(sentence): preferred.append(sentence)
        elif _REQUIRED_CUE.search(sentence) or extract_skills(sentence): required.append(sentence)
    return {"required":" ".join(required),"preferred":" ".join(preferred)}

def _generic_terms(text: str) -> set[str]:
    """Extract job-specific competency phrases when they are explicitly framed as skills."""
    terms=set()
    cue=re.compile(r"\b(?:experience (?:with|in)|proficiency in|expertise in|knowledge of|familiarity with|ability to|skilled in|background in|working knowledge of)\s+([^.;\n]+)",re.I)
    for match in cue.finditer(text):
        chunk=match.group(1)
        # Split coordinated lists without inventing arbitrary n-grams.
        for part in re.split(r",|\s+and\s+|\s+or\s+|/",chunk,flags=re.I):
            phrase=re.sub(r"[^A-Za-z0-9+#&./ -]"," ",part).strip(" -")
            toks=[t.lower() for t in TOKEN_RE.findall(phrase) if t.lower() not in GENERIC_REQUIREMENT_WORDS]
            if 2<=len(toks)<=6 and toks:
                terms.add(" ".join(toks))
    return terms

def _requirement_terms(text: str) -> list[str]:
    # Known competencies are canonical and preferred over generic phrases.
    known=extract_skills(text)
    generic=_generic_terms(text)
    known_lower={_norm for _norm in (x.lower() for x in known)}
    generic={g for g in generic if g not in known_lower and len(g.split())>=2}
    return known + sorted(generic, key=lambda x:(-len(x.split()),x))[:24]


def _term_present(term: str, text: str) -> bool:
    canonical = normalize_skill(term)
    if canonical in ALL_SKILLS:
        return any(_pattern(alias).search(text) for alias in aliases_for(canonical))
    return bool(_pattern(term).search(text))


def _term_patterns(term: str) -> list[re.Pattern[str]]:
    """Return canonical + alias patterns for a competency term.

    Generic JD phrases still use an exact phrase pattern. Canonical skills, however,
    must be searched through their complete alias set so that e.g. ``REST APIs``
    correctly provides evidence for canonical ``REST API``.
    """
    canonical = normalize_skill(term)
    if canonical in ALL_SKILLS:
        return [_pattern(alias) for alias in aliases_for(canonical)]
    return [_pattern(term)]


def _evidence_for_term(term: str, resume_text: str) -> dict[str,Any]:
    sections=_split_resume_sections(resume_text)
    patterns=_term_patterns(term)
    locations=[]
    for section, lines in sections.items():
        if section == "other":
            continue
        section_text=" ".join(lines)
        if any(pattern.search(section_text) for pattern in patterns):
            locations.append(section)
    if "experience" in locations or "projects" in locations or "research" in locations or "publications" in locations:
        level="strong"
    elif any(x in locations for x in ("summary","certifications","education","leadership","achievements","volunteering")):
        level="moderate"
    elif "skills" in locations:
        level="listed"
    else:
        level="weak"
    return {"locations":locations,"evidence_level":level}


def _keyword_coverage(resume_text: str, job_description: str) -> float:
    jd_terms=[t for t in _requirement_terms(job_description) if len(t.split())>=2]
    if not jd_terms: return 100.0
    return round(sum(_term_present(t,resume_text) for t in jd_terms)/len(jd_terms)*100,2)


def calculate_job_match(resume_text: str, resume_skills: list[str], required_skills: list[str], preferred_skills: list[str], job_description: str="") -> dict[str,Any]:
    resume_set={normalize_skill(x) for x in resume_skills}
    jd_sections=parse_job_sections(job_description)
    required_set={normalize_skill(x) for x in required_skills}
    preferred_set={normalize_skill(x) for x in preferred_skills}
    if not required_set and not preferred_set:
        required_set={normalize_skill(x) for x in extract_skills(jd_sections["required"])}
        preferred_set={normalize_skill(x) for x in extract_skills(jd_sections["preferred"])}
    preferred_set-=required_set
    # Add non-vocabulary requirements so the matcher works outside technical roles.
    required_generic=[x for x in _requirement_terms(jd_sections["required"]) if normalize_skill(x).lower() not in {s.lower() for s in required_set} and len(x.split())>=2]
    preferred_generic=[x for x in _requirement_terms(jd_sections["preferred"]) if normalize_skill(x).lower() not in {s.lower() for s in preferred_set} and len(x.split())>=2]
    required_items=[(x,"skill") for x in sorted(required_set)] + [(x,"phrase") for x in required_generic[:18]]
    preferred_items=[(x,"skill") for x in sorted(preferred_set)] + [(x,"phrase") for x in preferred_generic[:12]]
    def evaluate(items):
        matched=[]; missing=[]; evidence={}; points=0.0
        for term,kind in items:
            present = normalize_skill(term) in resume_set if kind=="skill" else _term_present(term,resume_text)
            if present:
                display=normalize_skill(term) if kind=="skill" else term
                matched.append(display); ev=_evidence_for_term(display,resume_text); evidence[display]=ev
                points += {"strong":1.0,"moderate":0.85,"listed":0.65,"weak":0.5}.get(ev["evidence_level"],0.5)
            else: missing.append(normalize_skill(term) if kind=="skill" else term)
        coverage=(len(matched)/len(items)*100) if items else 100.0
        evidence_score=(points/len(items)*100) if items else 100.0
        return matched,missing,evidence,coverage,evidence_score
    rm,rx,revidence,rcov,revidence_score=evaluate(required_items)
    pm,px,pevidence,pcov,pevidence_score=evaluate(preferred_items)
    keyword=_keyword_coverage(resume_text,job_description)
    # Required coverage is the core signal. Evidence is a smaller modifier so a
    # listed skill can match without being falsely treated as equivalent to experience.
    if required_items:
        score=rcov*0.60 + revidence_score*0.22 + (pcov if preferred_items else 100)*0.08 + keyword*0.10
    elif preferred_items:
        score=pcov*0.55 + pevidence_score*0.25 + keyword*0.20
    else:
        score=keyword
    total=len(required_items)+len(preferred_items)
    quality="high" if total>=5 else "medium" if total>=2 else "low"
    return {
      "job_match_score":round(max(0,min(100,score)),2), "signal_quality":quality,
      "required":{"matched":rm,"missing":rx,"matched_count":len(rm),"total_count":len(required_items),"coverage_percent":round(rcov,2)},
      "preferred":{"matched":pm,"missing":px,"matched_count":len(pm),"total_count":len(preferred_items),"coverage_percent":round(pcov,2)},
      "evidence":{**revidence,**pevidence}, "keyword_coverage":keyword,
      "method":"requirement coverage weighted toward required qualifications, with evidence location and job-specific terminology; no inferred years of experience",
    }

# Backwards-compatible legacy helper. The application should use calculate_job_match.
def calculate_ats_score(resume_skills:list[str], required_skills:list[str], preferred_skills:list[str])->dict[str,Any]:
    resume={normalize_skill(x) for x in resume_skills}; required={normalize_skill(x) for x in required_skills}; preferred={normalize_skill(x) for x in preferred_skills}-required
    earned=len(resume&required)+0.5*len(resume&preferred); possible=len(required)+0.5*len(preferred)
    score=round(earned/possible*100,2) if possible else 100.0
    return {"ats_score":score,"required":{"matched":sorted(resume&required),"missing":sorted(required-resume)},"preferred":{"matched":sorted(resume&preferred),"missing":sorted(preferred-resume)}}
