"""Universal resume-quality analysis independent of a job description."""
from __future__ import annotations
import re
from typing import Any

GENERIC_RE=re.compile(r"\b(responsible for|worked on|helped with|involved in|assisted with|duties included|tasked with|participated in)\b",re.I)
QUANT_RE=re.compile(r"(?:\b\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?\s?(?:k|m|million|thousand|users?|clients?|customers?|projects?|people|employees?)\b|[$€£₹]\s?\d|\b(?:increased|decreased|reduced|grew|improved|saved|cut|raised)\b[^.\n]{0,80}\b\d+)",re.I)
ACTION_RE=re.compile(r"\b(achieved|analyzed|automated|built|coordinated|created|delivered|designed|developed|directed|implemented|improved|increased|launched|led|managed|migrated|negotiated|optimized|organized|reduced|resolved|researched|scaled|streamlined|taught|trained|wrote|presented)\b",re.I)
DATE_TOKEN_RE=re.compile(r"\b(?:19|20)\d{2}\b")

def _clamp(v): return max(0,min(100,round(v,2)))

def analyze_resume_health(document:dict[str,Any])->dict[str,Any]:
    text=document["text"]; lines=[x.strip() for x in text.splitlines() if x.strip()]
    bullets=[x for x in lines if re.match(r"^\s*(?:[-*•▪◦‣–—]|\d+[.)]|[a-z][.)])\s+",x)]
    quantified=sum(bool(QUANT_RE.search(x)) for x in bullets); generic=sum(bool(GENERIC_RE.search(x)) for x in bullets); action=sum(bool(ACTION_RE.search(x)) for x in bullets)
    sections=set(document["section_names"]); stage=document.get("career_stage","unknown")
    contact=100 if document["email_detected"] and document["phone_detected"] else 65 if document["email_detected"] or document["phone_detected"] else 25
    # Completeness is contextual: projects/research can be a valid primary evidence
    # section for students and researchers; experience is not mandatory for everyone.
    core=0; core+=25 if "education" in sections else 0; core+=25 if "experience" in sections else 0; core+=20 if "skills" in sections else 0
    core+=15 if "projects" in sections or "research" in sections else 0; core+=10 if "certifications" in sections else 0; core+=5 if "achievements" in sections else 0
    completeness=_clamp(core*0.55+contact*0.35+(10 if document.get("url_count",0) else 0))
    structure=55+min(25,document["standard_section_count"]*5)+min(10,document["date_count"]*2)+min(10,document["bullet_count"]*1.5)
    structure-=8 if document["header_footer_signal"] else 0; structure-=8 if document["likely_two_column"] else 0
    structure=_clamp(structure)
    word_count=document["word_count"]
    content=82
    if word_count<150: content-=25
    elif word_count<250: content-=10
    if word_count>1600: content-=18
    elif word_count>1200: content-=8
    if document["replacement_character_count"]: content-=10
    content=_clamp(content)
    evidence=58
    if bullets:
        evidence+=min(28,quantified/len(bullets)*45)
        evidence+=min(12,action/len(bullets)*15)
        evidence-=min(22,generic/len(bullets)*30)
    else: evidence-=20
    evidence=_clamp(evidence)
    clarity=82
    if generic: clarity-=min(22,generic/max(len(bullets),1)*28)
    if document["replacement_character_count"]: clarity-=10
    if document["header_footer_signal"]: clarity-=5
    clarity=_clamp(clarity)
    cats={"content":content,"structure":structure,"completeness":completeness,"clarity":clarity,"evidence":evidence}
    score=_clamp(content*.22+structure*.20+completeness*.20+clarity*.16+evidence*.22)
    issues=[]; rec=[]
    if not document["email_detected"]: issues.append({"severity":"high","category":"completeness","message":"No email address was detected."})
    if not document["phone_detected"]: issues.append({"severity":"medium","category":"completeness","message":"No phone number was detected."})
    if "skills" not in sections: issues.append({"severity":"medium","category":"completeness","message":"No conventional skills/competencies section was detected; this is worth adding when relevant to the target field."})
    if stage=="experienced" and "experience" not in sections: issues.append({"severity":"high","category":"structure","message":"A professional experience section was not detected for a resume that appears to represent an experienced candidate."})
    elif stage=="student_or_entry_level" and "experience" not in sections and not ({"projects","research"}&sections): issues.append({"severity":"medium","category":"structure","message":"No experience, project, or research section was detected."})
    if bullets and quantified/max(len(bullets),1)<.15: issues.append({"severity":"medium","category":"evidence","message":"Few accomplishment bullets contain measurable outcomes, scale, scope, or other concrete evidence."})
    if bullets and generic/max(len(bullets),1)>.25: issues.append({"severity":"medium","category":"clarity","message":"Several bullets rely on generic responsibility language instead of specific actions and outcomes."})
    if word_count<150: issues.append({"severity":"high","category":"content","message":"Very little machine-readable content was detected; confirm that the resume is complete."})
    if word_count>1600: issues.append({"severity":"low","category":"content","message":"The resume is unusually long; remove low-value detail if it does not support the target role."})
    if quantified/max(len(bullets),1)<.15 and bullets: rec.append("Add truthful numbers, scope, outcomes, time saved, revenue, users, quality, or other concrete evidence to the strongest bullets.")
    if generic/max(len(bullets),1)>.25 and bullets: rec.append("Replace generic responsibility phrases with a specific action, context, and result.")
    if "skills" not in sections: rec.append("Add a concise competencies or skills section using terminology supported by the rest of the resume.")
    if not (document.get("linkedin_detected",False) or document.get("github_detected",False) or document.get("portfolio_detected",False)): rec.append("Consider adding one relevant professional or portfolio link when appropriate for the field.")
    return {"score":score,"categories":cats,"issues":issues,"recommendations":rec[:6],"signals":{"career_stage":stage,"bullet_count":len(bullets),"quantified_bullet_count":quantified,"generic_bullet_count":generic,"action_led_bullet_count":action,"word_count":word_count},"method":"deterministic, context-aware resume-quality heuristics; independent of the supplied job description"}
