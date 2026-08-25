import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from backend/.env
load_dotenv()

# Initialize client
client = None


def init_client():
    """Initialize Groq client using the API key from .env."""
    global client

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return False

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    return True


def analyze_with_ai(
    resume_text: str,
    job_description: str,
    scoring: dict
) -> dict | None:
    """
    Analyze a resume against a job description using Groq.

    The ATS score remains deterministic.
    Groq is only responsible for qualitative AI analysis.
    """

    if not client:
        if not init_client():
            return None

    try:
        prompt = f"""
Analyze this resume against the job description.

IMPORTANT:
The ATS score below was calculated by a deterministic scoring
system. Do NOT recalculate or change the ATS score.

RESUME:
{resume_text[:5000]}

JOB DESCRIPTION:
{job_description[:5000]}

DETERMINISTIC ATS RESULTS:

ATS Score:
{scoring["ats_score"]}%

Required Skills Matched:
{", ".join(scoring["required"]["matched"]) or "None"}

Required Skills Missing:
{", ".join(scoring["required"]["missing"]) or "None"}

Preferred Skills Matched:
{", ".join(scoring["preferred"]["matched"]) or "None"}

Preferred Skills Missing:
{", ".join(scoring["preferred"]["missing"]) or "None"}


Analyze the candidate's fit for the job.

Return ONLY valid JSON using exactly this structure:

{{
    "summary": "Brief 2-3 sentence summary of the candidate's overall fit.",

    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],

    "weaknesses": [
        "Weakness 1",
        "Weakness 2"
    ],

    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],

    "experience_relevance": "Explain how relevant the candidate's experience is to this role.",

    "skill_gap_analysis": "Explain the important missing skills and how they affect the candidate's fit."
}}

Do not include Markdown.
Do not include ```json.
Return only the JSON object.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=1200
        )

        ai_text = response.choices[0].message.content

        if not ai_text:
            return None

        # Remove accidental Markdown fences if the model adds them
        ai_text = ai_text.strip()

        if ai_text.startswith("```json"):
            ai_text = ai_text[7:]

        if ai_text.startswith("```"):
            ai_text = ai_text[3:]

        if ai_text.endswith("```"):
            ai_text = ai_text[:-3]

        ai_text = ai_text.strip()

        return json.loads(ai_text)

    except Exception as e:
        print(f"AI analysis failed: {e}")
        return None