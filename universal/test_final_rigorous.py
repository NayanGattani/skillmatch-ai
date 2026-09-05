import random
import string

from services import extract_skills, parse_job_sections, calculate_job_match, _evidence_for_term
from resume_health import analyze_resume_health
from ai_service import _validate_output, _build_prompt


def match(resume, jd):
    return calculate_job_match(resume, extract_skills(resume), [], [], jd)


def test_finance_resume_and_jd():
    resume = """PROFESSIONAL EXPERIENCE
Financial Analyst | 2023-2026
- Built financial models and forecasts for quarterly planning.
- Managed stakeholder reporting and budgeting.
SKILLS
Excel, Power BI, financial modeling, FP&A, valuation
"""
    jd = """Required Qualifications:
Experience with financial modeling, FP&A and Excel.
Strong stakeholder management and forecasting skills.
Preferred Qualifications:
Power BI and valuation.
"""
    r = match(resume, jd)
    assert set(r["required"]["missing"]) == {"stakeholder management"}
    assert r["evidence"]["financial modeling"]["evidence_level"] == "strong"
    assert r["evidence"]["FP&A"]["evidence_level"] == "listed"
    assert "stakeholder reporting" not in r["required"]["matched"]


def test_marketing_does_not_extract_strategy_from_content_strategy():
    assert extract_skills("Experience with content strategy and campaign management") == ["campaign management", "content strategy"]


def test_mechanical_aliases():
    r = match("EXPERIENCE\nDesigned parts using SolidWorks and GD&T.\n", "Required: SolidWorks and geometric dimensioning and tolerancing (GD&T).")
    assert r["required"]["matched_count"] == r["required"]["total_count"]


def test_healthcare_credentials_are_contextual_not_cs_specific():
    r = match("CERTIFICATIONS\nRegistered Nurse license\nEXPERIENCE\nProvided patient care and clinical documentation.\n", "Required: patient care and clinical documentation. Preferred: EMR.")
    assert "patient care" in r["required"]["matched"]


def test_legal_resume():
    r = match("EXPERIENCE\nPerformed legal research and contract review.\n", "Required: legal research and contract review. Preferred: due diligence.")
    assert set(r["required"]["matched"]) >= {"contract review", "legal research"}


def test_education_resume():
    r = match("TEACHING EXPERIENCE\nDeveloped lesson plans and managed classrooms.\n", "Required: lesson planning and classroom management.")
    assert r["required"]["matched_count"] == 2


def test_missing_required_is_not_hidden_by_keyword_overlap():
    r = match("SKILLS\nPython, Excel\n", "Required: Python, SQL, Docker")
    assert "SQL" in r["required"]["missing"]
    assert "Docker" in r["required"]["missing"]
    assert r["job_match_score"] < 90


def test_preferred_does_not_become_required():
    r = match("SKILLS\nPython\n", "Required: Python\nPreferred: Docker, AWS")
    assert r["required"]["missing"] == []
    assert set(r["preferred"]["missing"]) == {"AWS", "Docker"}


def test_negated_requirement_is_not_required():
    sections = parse_job_sections("Python is required. Docker is not required.")
    assert "Python" in extract_skills(sections["required"])
    assert "Docker" not in extract_skills(sections["required"])


def test_rest_alias_is_strong_when_in_project():
    ev = _evidence_for_term("REST API", "PROJECTS\nBuilt RESTful APIs for a booking service.\nSKILLS\nREST API\n")
    assert ev == {"locations": ["projects", "skills"], "evidence_level": "strong"}


def test_listed_only_never_becomes_strong():
    ev = _evidence_for_term("Docker", "PROFILE\nBackend developer.\nSKILLS\nDocker\n")
    assert ev["evidence_level"] == "listed"


def test_achievement_and_publication_sections_are_detected():
    ev = _evidence_for_term("research methodology", "PUBLICATIONS\nApplied research methodology in a peer-reviewed study.\nACHIEVEMENTS\nWon award.\n")
    assert ev["evidence_level"] == "strong"


def test_student_projects_do_not_trigger_missing_experience_high_warning():
    d={"text":"EDUCATION\nBSc\nPROJECTS\nBuilt a capstone.\nSKILLS\nPython", "section_names":["education","projects","skills"], "word_count":20,"email_detected":True,"phone_detected":True,"standard_section_count":3,"date_count":0,"bullet_count":1,"header_footer_signal":False,"likely_two_column":False,"replacement_character_count":0,"url_count":0,"linkedin_detected":False,"github_detected":False,"portfolio_detected":False,"career_stage":"student_or_entry_level"}
    h=analyze_resume_health(d)
    assert not any(x["severity"]=="high" and x["category"]=="structure" for x in h["issues"])


def test_experienced_resume_without_experience_is_flagged():
    d={"text":"PROFILE\nSenior manager.\nSKILLS\nOperations", "section_names":["summary","skills"], "word_count":20,"email_detected":True,"phone_detected":True,"standard_section_count":2,"date_count":5,"bullet_count":0,"header_footer_signal":False,"likely_two_column":False,"replacement_character_count":0,"url_count":0,"linkedin_detected":False,"github_detected":False,"portfolio_detected":False,"career_stage":"experienced"}
    h=analyze_resume_health(d)
    assert any(x["severity"]=="high" and x["category"]=="structure" for x in h["issues"])


def test_ai_validator_rejects_listed_skill_hands_on_claim():
    analysis={"scoring":{"evidence":{"Docker":{"locations":["skills"],"evidence_level":"listed"}}}}
    bad={"summary":"Strong Docker hands-on experience.","strengths":[],"weaknesses":[],"recommendations":[],"experience_relevance":"","skill_gap_analysis":""}
    assert _validate_output(bad, analysis) is None


def test_ai_validator_accepts_conservative_interpretation():
    analysis={"scoring":{"evidence":{"Docker":{"locations":["skills"],"evidence_level":"listed"}}}}
    good={"summary":"Docker is listed, but practical use is not demonstrated.","strengths":[],"weaknesses":["Docker lacks project evidence."],"recommendations":["Describe Docker usage if it was actually used."],"experience_relevance":"","skill_gap_analysis":"Docker is listed only."}
    assert _validate_output(good, analysis) == good


def test_ai_prompt_contains_evidence_contract():
    p=_build_prompt("SKILLS\nDocker", "Required: Docker", {"scoring":{"evidence":{"Docker":{"evidence_level":"listed"}}},"ats":{},"resume_health":{}})
    assert "listed' = found only in skills/competencies" in p
    assert "deterministic evidence map as authoritative" in p


def test_score_bounds_under_random_inputs():
    vocab=["Python","Excel","SEO","SolidWorks","patient care","contract review","teaching","financial modeling","Docker","AWS"]
    for _ in range(250):
        resume="SKILLS\n"+", ".join(random.sample(vocab,k=random.randint(0,len(vocab))))
        jd="Required: "+", ".join(random.sample(vocab,k=random.randint(1,min(5,len(vocab)))))
        r=match(resume,jd)
        assert 0 <= r["job_match_score"] <= 100
        assert 0 <= r["required"]["coverage_percent"] <= 100


def test_adversarial_text_does_not_crash():
    chars=string.ascii_letters+string.digits+" ,.;:/+&#-()\n"
    resume="".join(random.choice(chars) for _ in range(20000))
    jd="Required: Python, Excel, stakeholder management. "+resume[:3000]
    r=match(resume,jd)
    assert 0 <= r["job_match_score"] <= 100
