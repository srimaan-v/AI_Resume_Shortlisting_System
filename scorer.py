
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def calculate_score(resume_text, job_role, job_templates):
    template = job_templates[job_role]

    required_skills = template["required_skills"]
    preferred_skills = template["preferred_skills"]
    education = template["education"]
    certifications = template["certifications"]
    weights = template["weights"]

    resume_text = resume_text.lower()

    def count_matches(items):
        count = 0
        for item in items:
            if item.lower() in resume_text:
                count += 1
        return count

    required_match = count_matches(required_skills)
    preferred_match = count_matches(preferred_skills)
    education_match = count_matches(education)
    certification_match = count_matches(certifications)

    skill_score = (
        (required_match / max(len(required_skills), 1)) * weights["skills"] * 0.7 +
        (preferred_match / max(len(preferred_skills), 1)) * weights["skills"] * 0.3
    )

    education_score = (
        education_match / max(len(education), 1)
    ) * weights["education"]

    certification_score = (
        certification_match / max(len(certifications), 1)
    ) * weights["certifications"]

    experience_score = weights["experience_projects"] * 0.8

    academic_gap_penalty = 0
    gap_patterns = [
        r"gap",
        r"career break",
        r"year gap"
    ]

    for pattern in gap_patterns:
        if re.search(pattern, resume_text):
            academic_gap_penalty = weights["academic_gap"]
            break

    final_score = (
        skill_score +
        education_score +
        certification_score +
        experience_score -
        academic_gap_penalty
    )

    return max(final_score, 0)

