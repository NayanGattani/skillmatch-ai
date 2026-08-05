from skills import ALL_SKILLS

def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text by matching against our skill database.
    Case-insensitive.
    """
    found_skills = []
    text_lower = text.lower()
    
    for skill in ALL_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    # Remove duplicates and return sorted
    return sorted(list(set(found_skills)))

def calculate_ats_score(resume_skills: list[str], job_skills: list[str]) -> dict:
    """
    Calculate ATS score based on skill matching.
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    
    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set
    
    if len(job_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_set)) * 100)
    
    return {
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "ats_score": score,
        "matched_count": len(matched),
        "total_required": len(job_set)
    }