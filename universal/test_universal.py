from services import extract_skills, parse_job_sections, calculate_job_match
from resume_health import analyze_resume_health


def test_non_cs_competencies_are_detected():
    jd = "Required qualifications: financial modeling, Excel, forecasting, stakeholder management. Preferred: Power BI."
    sections = parse_job_sections(jd)
    assert {"financial modeling","Excel","forecasting","stakeholder management"} <= set(extract_skills(sections["required"]))
    assert "Power BI" in extract_skills(sections["preferred"])


def test_unlisted_job_specific_phrase_is_matchable():
    jd = "Required: Experience with procurement and contract negotiation. Ability to manage vendors."
    resume = "PROFESSIONAL EXPERIENCE\nManaged procurement and vendor relationships.\nLed contract negotiation for suppliers."
    result = calculate_job_match(resume, extract_skills(resume), [], [], jd)
    assert result["required"]["matched_count"] >= 2
    assert result["job_match_score"] >= 50


def test_student_projects_are_not_treated_as_missing_experience():
    document = {
        "text":"NAME\nme@example.com +91 9999999999\nEDUCATION\nBSc\nPROJECTS\nBuilt a research project.\nSKILLS\nPython SQL",
        "section_names":["education","projects","skills"],"word_count":25,"email_detected":True,"phone_detected":True,
        "standard_section_count":3,"date_count":0,"bullet_count":1,"header_footer_signal":False,"likely_two_column":False,
        "replacement_character_count":0,"control_character_count":0,"url_count":0,"linkedin_detected":False,"github_detected":False,"portfolio_detected":False,
        "career_stage":"student_or_entry_level","text_extractable":True,"tables":0,"image_only_pages":0,
    }
    result=analyze_resume_health(document)
    assert not any(i["category"]=="structure" and i["severity"]=="high" for i in result["issues"])


def test_skill_evidence_uses_aliases_in_project_text():
    from services import _evidence_for_term
    resume = """Profile\nBackend developer\nProjects\nBuilt RESTful APIs for a service.\nTechnical Skills\nREST API\n"""
    evidence = _evidence_for_term("REST API", resume)
    assert "projects" in evidence["locations"]
    assert evidence["evidence_level"] == "strong"


def test_listed_skill_is_not_called_hands_on_by_evidence_layer():
    from services import _evidence_for_term
    resume = """Profile\nDeveloper\nProjects\nBuilt a web application.\nTechnical Skills\nDocker\n"""
    evidence = _evidence_for_term("Docker", resume)
    assert evidence["locations"] == ["skills"]
    assert evidence["evidence_level"] == "listed"

def test_longer_competency_phrase_does_not_create_shorter_overlap():
    assert extract_skills("Required: content strategy and campaign management") == ["campaign management", "content strategy"]


def test_universal_evidence_buckets_include_achievements_and_languages():
    from services import _split_resume_sections
    sections = _split_resume_sections("ACHIEVEMENTS\nWon first place.\nLANGUAGES\nEnglish, Hindi")
    assert sections["achievements"] == ["Won first place."]
    assert sections["languages"] == ["English, Hindi"]
