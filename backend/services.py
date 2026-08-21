import re
from skills import ALL_SKILLS, normalize_skill

def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text using regex word boundaries.
    
    Handles:
    - Single word skills: Python, Docker
    - Multi-word skills: REST API, Unit Testing
    - Punctuated skills: C++, C#, Node.js, CI/CD
    - Plural forms: REST APIs → REST API, Dockers → Docker
    - Case insensitive matching
    - Returns canonical skill names only
    """
    if not text:
        return []
    
    found_skills = set()
    text_lower = text.lower()
    
    # For each skill, create primary and plural patterns
    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        
        # Create primary pattern based on skill structure
        if " " in skill_lower:
            # Multi-word skill: "REST API" → r"rest\s+api"
            pattern = r"\b" + r"\s+".join(skill_lower.split()) + r"\b"
        elif any(c in skill_lower for c in ["+", "#", "."]):
            # Punctuated skill: "C++" → r"c\+\+"
            pattern = re.escape(skill_lower)
            if skill_lower[0].isalnum():
                pattern = r"\b" + pattern
            if skill_lower[-1].isalnum():
                pattern = pattern + r"\b"
        else:
            # Single word: "Python" → r"\bpython\b"
            pattern = r"\b" + re.escape(skill_lower) + r"\b"
        
        # Search for primary pattern
        if re.search(pattern, text_lower):
            found_skills.add(skill)
        else:
            # Also try plural form for alphanumeric skills
            if skill_lower and skill_lower[-1].isalpha():
                if " " in skill_lower:
                    # Multi-word: "REST API" → "REST APIs"
                    words = skill_lower.split()
                    words[-1] = words[-1] + "s"
                    plural_pattern = r"\b" + r"\s+".join(words) + r"\b"
                else:
                    # Single word: "Docker" → "Dockers"
                    plural_pattern = r"\b" + re.escape(skill_lower) + r"s\b"
                
                if re.search(plural_pattern, text_lower):
                    found_skills.add(skill)
    
    # Normalize aliases
    normalized = set()
    for skill in found_skills:
        canonical = normalize_skill(skill)
        normalized.add(canonical)
    
    return sorted(list(normalized))


def parse_job_sections(job_description: str) -> dict:
    """
    Parse job description to extract Required and Preferred sections.
    
    First tries to find explicit section headers.
    If no headers found, falls back to keyword-based heuristic.
    """
    text = job_description
    text_lower = text.lower()
    
    required_section = ""
    preferred_section = ""
    
    # Try explicit section headers first
    required_start = -1
    for keyword in ["requirements:", "required skills:", "must have:", "mandatory:"]:
        idx = text_lower.find(keyword)
        if idx != -1:
            required_start = idx + len(keyword)
            break
    
    preferred_start = -1
    for keyword in ["preferred:", "preferred skills:", "nice to have:", "bonus:", "advantageous:"]:
        idx = text_lower.find(keyword)
        if idx != -1:
            preferred_start = idx + len(keyword)
            break
    
    # Extract sections based on explicit headers
    if required_start != -1:
        if preferred_start != -1:
            required_section = job_description[required_start:preferred_start]
        else:
            required_section = job_description[required_start:]
    
    if preferred_start != -1:
        preferred_section = job_description[preferred_start:]
    
    # If no sections found, use fallback heuristic
    if not required_section and not preferred_section:
        required_section, preferred_section = _fallback_section_parsing(job_description)
    
    return {
        "required": required_section.strip(),
        "preferred": preferred_section.strip()
    }


def _fallback_section_parsing(job_description: str) -> tuple[str, str]:
    """
    Fallback parsing for paragraph-style JDs without explicit headers.
    
    Classifies skills based on nearby keywords:
    - Required indicators: "must have", "required", "essential", "mandatory"
    - Preferred indicators: "nice to have", "bonus", "plus", "preferred"
    
    Returns (required_text, preferred_text)
    """
    required_keywords = r"\b(must have|required|essential|mandatory|need|important)\b"
    preferred_keywords = r"\b(nice to have|bonus|plus|preferred|advantageous|advantage)\b"
    
    sentences = job_description.split(".")
    
    required_parts = []
    preferred_parts = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_lower = sentence.lower()
        
        # Check for required/preferred indicators
        has_required = re.search(required_keywords, sentence_lower)
        has_preferred = re.search(preferred_keywords, sentence_lower)
        
        if has_required and not has_preferred:
            required_parts.append(sentence)
        elif has_preferred and not has_required:
            preferred_parts.append(sentence)
        elif has_required and has_preferred:
            # Sentence contains both - split by position
            required_match = re.search(required_keywords, sentence_lower)
            preferred_match = re.search(preferred_keywords, sentence_lower)
            
            if required_match.start() < preferred_match.start():
                required_parts.append(sentence)
            else:
                preferred_parts.append(sentence)
        else:
            # No explicit indicator - default to required if early in description
            if len(required_parts) == 0:
                required_parts.append(sentence)
            else:
                preferred_parts.append(sentence)
    
    return (" ".join(required_parts), " ".join(preferred_parts))


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