from services import extract_skills, parse_job_sections, calculate_ats_score

def test_false_positive_fix():
    """Test A: No false positives on common words"""
    text = "good communication skills"
    skills = extract_skills(text)
    assert "Go" not in skills, "False positive: 'Go' detected in 'good'"
    print("✅ Test A passed: No 'Go' false positive")

def test_c_variants():
    """Test B: C++, C#, C work correctly"""
    text = "proficient in C++, C#, and C"
    skills = extract_skills(text)
    assert "C++" in skills, "C++ not detected"
    assert "C#" in skills, "C# not detected"
    assert "C" in skills, "C not detected"
    print("✅ Test B passed: C++, C#, C all detected")

def test_alias_normalization():
    """Test C & D: Alias normalization"""
    # K8s → Kubernetes
    text1 = "experience with k8s and kubernetes"
    skills1 = extract_skills(text1)
    assert skills1.count("Kubernetes") == 1, "Kubernetes not normalized"
    assert "K8s" not in skills1, "K8s not normalized to Kubernetes"
    
    # Postgres → PostgreSQL
    text2 = "postgres and postgresql skills"
    skills2 = extract_skills(text2)
    assert skills2.count("PostgreSQL") == 1, "PostgreSQL not normalized"
    assert "postgres" not in skills2, "postgres not normalized"
    print("✅ Test C & D passed: Aliases normalized to canonical names")

def test_multiword_skills():
    """Test E: Multi-word skills including plurals"""
    text = "REST API and REST APIs and Unit Testing"
    skills = extract_skills(text)
    assert "REST API" in skills, "REST API not detected"
    assert "Unit Testing" in skills, "Unit Testing not detected"
    # Verify only canonical forms are returned, no duplicates
    assert skills.count("REST API") == 1, "REST API returned multiple times"
    print("✅ Test E passed: Multi-word skills including plurals detected")

def test_paragraph_parsing():
    """Test F: Paragraph-style JD fallback"""
    jd = """We're looking for a backend engineer with strong Python and SQL skills. 
    Experience with REST APIs is essential. Docker and AWS are a plus."""
    
    sections = parse_job_sections(jd)
    required = extract_skills(sections["required"])
    preferred = extract_skills(sections["preferred"])
    
    assert "Python" in required, "Python should be required"
    assert "SQL" in required, "SQL should be required"
    assert "REST API" in required, "REST API should be required"
    assert "AWS" in preferred, "AWS should be preferred"
    assert "Docker" in preferred, "Docker should be preferred"
    print("✅ Test F passed: Paragraph parsing works")

def test_weighted_score_unchanged():
    """Test G: Weighted scoring still works"""
    resume = ["Python", "SQL", "Docker", "AWS"]
    required = ["Python", "SQL", "REST API", "Docker"]
    preferred = ["AWS", "Kubernetes"]
    
    result = calculate_ats_score(resume, required, preferred)
    
    # Expected: 3/4 required + 1/2 preferred
    # Earned: 3 + 0.5 = 3.5
    # Possible: 4 + 1 = 5
    # Score: 70%
    
    assert result["ats_score"] == 70.0, f"Expected 70.0, got {result['ats_score']}"
    print("✅ Test G passed: Weighted scoring works correctly")

if __name__ == "__main__":
    test_false_positive_fix()
    test_c_variants()
    test_alias_normalization()
    test_multiword_skills()
    test_paragraph_parsing()
    test_weighted_score_unchanged()
    print("\n🎉 All tests passed!")