import re
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

def calculate_ats_score(resume_skills: list[str], required_skills: list[str], preferred_skills: list[str]) -> dict:
    """
    Calculate weighted ATS score.
    
    Required skills: weight 1.0
    Preferred skills: weight 0.5
    
    Score = (earned_points / possible_points) × 100
    """
    resume_set = set(resume_skills)
    required_set = set(required_skills)
    preferred_set = set(preferred_skills)
    
    # Find matches
    required_matched = resume_set.intersection(required_set)
    preferred_matched = resume_set.intersection(preferred_set)
    
    # Find missing
    required_missing = required_set - resume_set
    preferred_missing = preferred_set - resume_set
    
    # Calculate points
    earned_points = (len(required_matched) * 1.0) + (len(preferred_matched) * 0.5)
    possible_points = (len(required_set) * 1.0) + (len(preferred_set) * 0.5)
    
    # Calculate score
    if possible_points == 0:
        score = 0
    else:
        score = round((earned_points / possible_points) * 100, 2)
    
    return {
        "ats_score": score,
        "required": {
            "matched": sorted(list(required_matched)),
            "missing": sorted(list(required_missing)),
            "matched_count": len(required_matched),
            "total_count": len(required_set)
        },
        "preferred": {
            "matched": sorted(list(preferred_matched)),
            "missing": sorted(list(preferred_missing)),
            "matched_count": len(preferred_matched),
            "total_count": len(preferred_set)
        },
        "earnings": {
            "earned_points": earned_points,
            "possible_points": possible_points
        }
    }

def parse_job_sections(job_description: str) -> dict:
    """
    Split a job description into required and preferred sections.

    Recognizes common section headers with or without Markdown markers
    or a trailing colon.
    """

    text = job_description.lower()

    required_keywords = [
        "requirements",
        "required skills",
        "must have",
        "mandatory",
        "essential"
    ]

    preferred_keywords = [
        "preferred skills",
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus",
        "advantageous"
    ]

    required_start = -1
    preferred_start = -1

    # Find required section
    for keyword in required_keywords:
        idx = text.find(keyword)
        if idx != -1:
            required_start = idx + len(keyword)
            break

    # Find preferred section
    for keyword in preferred_keywords:
        idx = text.find(keyword)
        if idx != -1:
            preferred_start = idx + len(keyword)
            break

    required_section = ""
    preferred_section = ""

    if required_start != -1:
        if preferred_start != -1 and preferred_start > required_start:
            required_section = job_description[required_start:preferred_start]
        else:
            required_section = job_description[required_start:]

    if preferred_start != -1:
        preferred_section = job_description[preferred_start:]

    return {
        "required": required_section.strip(),
        "preferred": preferred_section.strip()
    }