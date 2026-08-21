import re
from skills import ALL_SKILLS, SKILL_ALIASES, normalize_skill


def _build_skill_pattern(skill: str) -> str:
    """
    Build a regex pattern that safely matches a skill.

    Handles:
    - Single words
    - Multi-word skills
    - Punctuation-heavy skills such as C++, C#, Node.js, CI/CD
    """

    skill_lower = skill.lower().strip()

    # Multi-word skill
    if " " in skill_lower:
        parts = skill_lower.split()

        pattern = r"\s+".join(re.escape(part) for part in parts)

        return r"(?<!\w)" + pattern + r"(?!\w)"

    # Skills containing punctuation
    if any(char in skill_lower for char in ["+", "#", ".", "/"]):
        pattern = re.escape(skill_lower)

        # Don't use \b because punctuation-heavy skills
        # can behave badly with normal word boundaries.
        return r"(?<!\w)" + pattern + r"(?!\w)"

    # Normal single-word skill
    return r"\b" + re.escape(skill_lower) + r"\b"


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text.

    Searches both canonical skills and aliases,
    then converts everything to canonical names.

    Example:
        K8s -> Kubernetes
        Postgres -> PostgreSQL
        ReactJS -> React
    """

    if not text:
        return []

    found_skills = set()

    # Search canonical skills
    searchable_skills = set(ALL_SKILLS)

    # Search aliases too
    searchable_skills.update(SKILL_ALIASES.keys())

    text_lower = text.lower()

    for skill in searchable_skills:

        pattern = _build_skill_pattern(skill)

        if re.search(pattern, text_lower):
            canonical = normalize_skill(skill)
            found_skills.add(canonical)

    return sorted(found_skills)


def parse_job_sections(job_description: str) -> dict:
    """
    Parse a job description into required and preferred sections.

    First attempts explicit section detection.

    If no explicit sections exist, falls back to
    sentence-level heuristic classification.
    """

    if not job_description:
        return {
            "required": "",
            "preferred": ""
        }

    text = job_description

    # Explicit section headers.
    #
    # We intentionally allow:
    # "Nice to have:"
    # "Nice to have"
    # "Nice to have experience with"
    # etc.
    required_patterns = [
        r"\brequirements?\s*:?",
        r"\brequired skills?\s*:?",
        r"\bmust have\s*:?",
        r"\bmandatory\s*:?",
        r"\bessential skills?\s*:?",
        r"\bminimum qualifications?\s*:?",
        r"\bbasic qualifications?\s*:?",
        r"\bkey qualifications?\s*:?"
    ]

    preferred_patterns = [
        r"\bpreferred skills?\s*:?",
        r"\bpreferred\s*:?",
        r"\bnice[- ]to[- ]have\s*:?",
        r"\bnice[- ]to[- ]have experience with\b",
        r"\bwould be great\s*:?",
        r"\bwould be a plus\s*:?",
        r"\bgood to have\s*:?",
        r"\bbonus\s*:?",
        r"\boptional\s*:?",
        r"\badvantageous\s*:?"
    ]

    required_match = _find_first_header(text, required_patterns)
    preferred_match = _find_first_header(text, preferred_patterns)

    required_section = ""
    preferred_section = ""

    # If explicit headers exist, use them.
    if required_match or preferred_match:

        if required_match:
            required_start = required_match.end()

            if preferred_match and preferred_match.start() > required_start:
                required_section = text[
                    required_start:preferred_match.start()
                ]
            else:
                required_section = text[required_start:]

        if preferred_match:
            preferred_start = preferred_match.end()
            preferred_section = text[preferred_start:]

        return {
            "required": required_section.strip(),
            "preferred": preferred_section.strip()
        }

    # No explicit headers.
    # Use fallback parsing.
    required_section, preferred_section = _fallback_section_parsing(text)

    return {
        "required": required_section.strip(),
        "preferred": preferred_section.strip()
    }


def _find_first_header(text: str, patterns: list[str]):
    """
    Find the earliest matching section header.
    """

    matches = []

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            matches.append(match)

    if not matches:
        return None

    return min(matches, key=lambda match: match.start())


def _fallback_section_parsing(job_description: str) -> tuple[str, str]:
    """
    Handle paragraph-style job descriptions.

    Classification rules:

    1. Explicit preferred language -> preferred
    2. Explicit required language -> required
    3. Explicit negation such as "not required" -> unclassified
    4. Otherwise, if the sentence contains known skills,
       treat it as required.

    This gives us a reasonable deterministic fallback without
    pretending to understand the full semantics of the JD.
    """

    sentences = re.split(r"(?<=[.!?])\s+", job_description)

    required_parts = []
    preferred_parts = []

    required_pattern = re.compile(
        r"\b(must have|required|essential|mandatory|need|important)\b",
        re.IGNORECASE
    )

    preferred_pattern = re.compile(
        r"\b(nice[- ]to[- ]have|bonus|plus|preferred|advantageous|"
        r"would be great|good to have)\b",
        re.IGNORECASE
    )

    negative_required_pattern = re.compile(
        r"\bnot\s+(required|mandatory|essential)\b",
        re.IGNORECASE
    )

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_lower = sentence.lower()

        # --------------------------------------------------
        # 1. Explicit preferred sentence
        # --------------------------------------------------

        preferred_match = preferred_pattern.search(sentence)

        if preferred_match:
            preferred_parts.append(sentence)
            continue

        # --------------------------------------------------
        # 2. Explicit "not required" sentence
        # --------------------------------------------------

        if negative_required_pattern.search(sentence_lower):
            # Do not classify this sentence as required.
            continue

        # --------------------------------------------------
        # 3. Explicit required sentence
        # --------------------------------------------------

        required_match = required_pattern.search(sentence)

        if required_match:
            required_parts.append(sentence)
            continue

        # --------------------------------------------------
        # 4. No explicit classification
        #
        # If the sentence contains recognized technical
        # skills, treat those skills as required.
        # --------------------------------------------------

        detected_skills = extract_skills(sentence)

        if detected_skills:
            required_parts.append(sentence)

    return (
        " ".join(required_parts),
        " ".join(preferred_parts)
    )


def calculate_ats_score(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str]
) -> dict:
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
    earned_points = (
        len(required_matched) * 1.0
        + len(preferred_matched) * 0.5
    )

    possible_points = (
        len(required_set) * 1.0
        + len(preferred_set) * 0.5
    )

    # Calculate score
    if possible_points == 0:
        score = 0
    else:
        score = round(
            (earned_points / possible_points) * 100,
            2
        )

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