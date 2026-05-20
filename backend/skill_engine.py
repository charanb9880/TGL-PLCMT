import re
from typing import Any


MATCH_FIELDS = [
    "Tech Stack/Tools Used",
    "AI/ML Adoption Level",
    "Automation level",
    "Skill relevance",
    "Services / Offerings / Products",
    "Focus Sectors / Industries",
    "Learning culture",
]


def normalize_skills(skills: list[str] | str) -> list[str]:
    if isinstance(skills, str):
        raw_skills = re.split(r"[,\n;/]", skills)
    else:
        raw_skills = skills

    return [skill.strip() for skill in raw_skills if skill and skill.strip()]


def keyword_list(value: Any) -> list[str]:
    if value is None:
        return []
    return [item.strip() for item in re.split(r"[,;/]", str(value)) if item.strip()]


def evaluate_skill_match(company: dict[str, Any], skills: list[str] | str) -> dict[str, Any]:
    requested_skills = normalize_skills(skills)
    corpus = " ".join(str(company.get(field, "")) for field in MATCH_FIELDS).lower()
    matched_skills = [skill for skill in requested_skills if skill.lower() in corpus]

    stack_keywords = keyword_list(company.get("Tech Stack/Tools Used"))
    sector_keywords = keyword_list(company.get("Focus Sectors / Industries"))
    missing_keywords = [
        keyword
        for keyword in stack_keywords + sector_keywords
        if keyword.lower() not in {skill.lower() for skill in requested_skills}
    ]

    adoption_text = str(company.get("AI/ML Adoption Level", "")).lower()
    automation_text = str(company.get("Automation level", "")).lower()
    relevance_text = str(company.get("Skill relevance", "")).lower()

    score = len(matched_skills) * 22
    if "high" in adoption_text or "very high" in adoption_text:
        score += 14
    if "high" in automation_text:
        score += 10
    if "high" in relevance_text or "extremely" in relevance_text:
        score += 12

    if score >= 60:
        fit_level = "High"
    elif score >= 35:
        fit_level = "Medium"
    else:
        fit_level = "Low"

    preparation_suggestions = []
    if stack_keywords:
        preparation_suggestions.append(
            f"Strengthen experience with: {', '.join(stack_keywords[:4])}."
        )
    if company.get("AI/ML Adoption Level"):
        preparation_suggestions.append(
            f"Prepare examples that align with the company's {company.get('AI/ML Adoption Level')} AI/ML adoption level."
        )
    if company.get("Learning culture"):
        preparation_suggestions.append(
            f"Frame your growth story around the company's learning culture: {company.get('Learning culture')}."
        )

    return {
        "fit_level": fit_level,
        "matched_skills": matched_skills,
        "skill_gaps": missing_keywords[:6],
        "preparation_suggestions": preparation_suggestions[:3],
        "match_score": min(score, 100),
        "evaluated_fields": MATCH_FIELDS,
    }