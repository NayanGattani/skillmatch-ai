from services import extract_skills, parse_job_sections, calculate_ats_score


# ============================================================
# TEST A — No false positive for "Go"
# ============================================================

def test_false_positive_fix():
    text = "good communication skills"

    skills = extract_skills(text)

    assert "Go" not in skills, \
        "False positive: 'Go' detected in 'good'"

    print("Test A passed: No 'Go' false positive")


# ============================================================
# TEST B — C, C++, C#
# ============================================================

def test_c_variants():
    text = "proficient in C++, C#, and C"

    skills = extract_skills(text)

    assert "C++" in skills, "C++ not detected"
    assert "C#" in skills, "C# not detected"
    assert "C" in skills, "C not detected"

    print("Test B passed: C++, C#, C all detected")


# ============================================================
# TEST C/D — Alias normalization
# ============================================================

def test_alias_normalization():

    text1 = "experience with k8s and kubernetes"

    skills1 = extract_skills(text1)

    assert "Kubernetes" in skills1
    assert "K8s" not in skills1
    assert skills1.count("Kubernetes") == 1

    text2 = "postgres and postgresql skills"

    skills2 = extract_skills(text2)

    assert "PostgreSQL" in skills2
    assert "Postgres" not in skills2
    assert skills2.count("PostgreSQL") == 1

    print("Test C & D passed: Aliases normalized to canonical names")


# ============================================================
# TEST E — Multi-word skills
# ============================================================

def test_multiword_skills():

    text = "REST API and Unit Testing"

    skills = extract_skills(text)

    assert "REST API" in skills
    assert "Unit Testing" in skills

    print("Test E passed: Multi-word skills detected")


# ============================================================
# TEST F — Paragraph parsing
# ============================================================

def test_paragraph_parsing():

    jd = """
    We're looking for a backend engineer with strong Python and SQL skills.
    Experience with REST APIs is essential.
    Docker and AWS are a plus.
    """

    sections = parse_job_sections(jd)

    required = extract_skills(sections["required"])
    preferred = extract_skills(sections["preferred"])

    assert "Python" in required
    assert "SQL" in required
    assert "REST API" in required

    assert "Docker" in preferred
    assert "AWS" in preferred

    print("Test F passed: Paragraph parsing works")


# ============================================================
# TEST G — Weighted scoring unchanged
# ============================================================

def test_weighted_score_unchanged():

    resume = [
        "Python",
        "SQL",
        "Docker",
        "AWS"
    ]

    required = [
        "Python",
        "SQL",
        "REST API",
        "Docker"
    ]

    preferred = [
        "AWS",
        "Kubernetes"
    ]

    result = calculate_ats_score(
        resume,
        required,
        preferred
    )

    # Required:
    # Python = 1
    # SQL = 1
    # Docker = 1
    # REST API = 0
    #
    # Preferred:
    # AWS = 0.5
    # Kubernetes = 0
    #
    # Earned = 3.5
    # Possible = 5
    # Score = 70%

    assert result["ats_score"] == 70.0, \
        f"Expected 70.0, got {result['ats_score']}"

    print("Test G passed: Weighted scoring works correctly")


# ============================================================
# TEST H — Nice-to-have without colon
# ============================================================

def test_preferred_phrase_without_colon():

    jd = """
    Required Skills:
    Python, SQL, Docker, Microservices, REST API

    Nice to have experience with AWS or GCP.
    """

    sections = parse_job_sections(jd)

    required = extract_skills(sections["required"])
    preferred = extract_skills(sections["preferred"])

    assert "Python" in required
    assert "SQL" in required
    assert "Docker" in required
    assert "Microservices" in required
    assert "REST API" in required

    assert "AWS" in preferred
    assert "GCP" in preferred

    assert "AWS" not in required
    assert "GCP" not in required

    print("Test H passed: Nice-to-have phrase detected")


# ============================================================
# TEST I — Would be great
# ============================================================

def test_would_be_great():

    jd = """
    Must Have:
    Python, FastAPI, PostgreSQL

    Would be great:
    Docker, Redis, Kubernetes
    """

    sections = parse_job_sections(jd)

    required = extract_skills(sections["required"])
    preferred = extract_skills(sections["preferred"])

    assert "Python" in required
    assert "FastAPI" in required
    assert "PostgreSQL" in required

    assert "Docker" in preferred
    assert "Redis" in preferred
    assert "Kubernetes" in preferred

    assert "Redis" not in required

    print("Test I passed: Would-be-great section detected")


# ============================================================
# TEST J — "Not required"
# ============================================================

def test_not_required():

    jd = """
    We're looking for a backend engineer with Python and SQL.
    Experience with REST APIs is essential.
    Knowledge of microservices architecture is valuable but not required.
    Docker and AWS are a plus.
    """

    sections = parse_job_sections(jd)

    required = extract_skills(sections["required"])
    preferred = extract_skills(sections["preferred"])

    assert "Python" in required
    assert "SQL" in required
    assert "REST API" in required

    assert "Microservices" not in required

    assert "Docker" in preferred
    assert "AWS" in preferred

    print("Test J passed: 'not required' handled correctly")


# ============================================================
# TEST K — Alias detection
# ============================================================

def test_alias_detection():

    text = """
    Experience with K8s, Kubernetes, Postgres, PostgreSQL,
    React.js, ReactJS, and REST APIs.
    """

    skills = extract_skills(text)

    assert "Kubernetes" in skills
    assert "PostgreSQL" in skills
    assert "React" in skills
    assert "REST API" in skills

    assert skills.count("Kubernetes") == 1
    assert skills.count("PostgreSQL") == 1
    assert skills.count("React") == 1
    assert skills.count("REST API") == 1

    assert "K8s" not in skills
    assert "Postgres" not in skills

    print("Test K passed: Aliases detected and normalized")


# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":

    test_false_positive_fix()
    test_c_variants()
    test_alias_normalization()
    test_multiword_skills()
    test_paragraph_parsing()
    test_weighted_score_unchanged()

    test_preferred_phrase_without_colon()
    test_would_be_great()
    test_not_required()
    test_alias_detection()

    print("\nAll V2.5 tests passed!")