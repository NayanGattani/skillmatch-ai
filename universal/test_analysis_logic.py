from ats_service import calculate_ats_readiness
from resume_health import analyze_resume_health
from services import calculate_job_match, extract_skills, parse_job_sections


def test_skill_aliases_and_boundaries():
    text = "Good communication. Built APIs with Python, K8s, Postgres, ReactJS and C++."
    skills = extract_skills(text)
    assert "Go" not in skills
    assert "Kubernetes" in skills
    assert "PostgreSQL" in skills
    assert "React" in skills
    assert "C++" in skills


def test_job_section_classification():
    jd = """
    Requirements:
    Python, FastAPI, PostgreSQL
    Experience building REST APIs is essential.

    Nice to have:
    Docker, AWS, Kubernetes
    """
    sections = parse_job_sections(jd)
    assert set(extract_skills(sections["required"])) >= {"Python", "FastAPI", "PostgreSQL", "REST API"}
    assert set(extract_skills(sections["preferred"])) >= {"Docker", "AWS", "Kubernetes"}


def test_job_match_rewards_demonstrated_required_skills():
    resume = """
    EXPERIENCE
    Built production FastAPI services in Python and PostgreSQL.
    PROJECTS
    Deployed REST APIs with Docker.
    SKILLS
    Python, FastAPI, PostgreSQL, Docker
    """
    result = calculate_job_match(
        resume,
        extract_skills(resume),
        ["Python", "FastAPI", "PostgreSQL", "REST API"],
        ["Docker"],
        "Python FastAPI PostgreSQL REST API Docker",
    )
    assert result["required"]["matched_count"] == 4
    assert result["job_match_score"] >= 85
    assert result["evidence"]["Python"]["evidence_level"] == "strong"


def test_ats_readiness_is_not_job_match():
    document = {
        "text": "JOHN DOE\njohn@example.com +91 9876543210\nEXPERIENCE\nBuilt systems.\nEDUCATION\nB.Tech\nSKILLS\nPython SQL",
        "text_extractable": True,
        "standard_section_count": 3,
        "email_detected": True,
        "phone_detected": True,
        "replacement_character_count": 0,
        "control_character_count": 0,
        "likely_two_column": False,
        "tables": 0,
        "header_footer_signal": False,
        "image_only_pages": 0,
        "section_names": ["experience", "education", "skills"],
        "word_count": 30,
        "bullet_count": 0,
        "date_count": 2,
        "unique_character_ratio": 0.2,
    }
    ats = calculate_ats_readiness(document)
    health = analyze_resume_health(document)
    assert 0 <= ats["score"] <= 100
    assert 0 <= health["score"] <= 100
    assert ats["method"] != health["method"]
