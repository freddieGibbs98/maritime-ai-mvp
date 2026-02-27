# main.py
# Einfaches lokales Python-Skript zur Analyse einer Inspektionsbeschreibung
# Ausgabe: Summary, Risk Level, Recommended Action

import re
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    summary: str
    risk_level: str
    recommended_action: str


HIGH_RISK_KEYWORDS = [
    "crack", "fire", "leak", "gas", "short circuit", "overheating",
    "smoke", "burn", "structural damage", "advanced corrosion", "severe corrosion", "heavy corrosion"
]
CRITICAL_HIGH_KEYWORDS = [
    "fire", "explosion", "flood"
]

MEDIUM_RISK_KEYWORDS = [
    "wear", "loose", "noise", "vibration", "minor leak",
    "rust", "degraded", "misaligned",
    "corroded", "corroding", "corrosion"
]

LOW_RISK_KEYWORDS = [
    "dust", "dirty", "cosmetic", "paint", "label missing"
]


def normalize(text: str) -> str:
    return text.lower().strip()


def count_keyword_hits(text: str, keywords: list[str]) -> int:
    hits = 0
    for kw in keywords:
        # einfache Wort-/Phrasensuche
        if re.search(r"\b" + re.escape(kw) + r"\b", text):
            hits += 1
    return hits


def build_summary(text: str, max_len: int = 160) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "..."


def determine_risk(text:str) -> tuple[str, int, int, int]:
    high_hits = count_keyword_hits(text, HIGH_RISK_KEYWORDS)
    med_hits = count_keyword_hits(text, MEDIUM_RISK_KEYWORDS)
    low_hits = count_keyword_hits(text, LOW_RISK_KEYWORDS)
    critical_hits = count_keyword_hits(text, CRITICAL_HIGH_KEYWORDS)
    if critical_hits > 0:
        return "HIGH", high_hits, med_hits, low_hits
    elif high_hits >= 2:
        return "HIGH", high_hits, med_hits, low_hits 
    elif med_hits > 0:
        return "MEDIUM", high_hits, med_hits, low_hits
    else:
        return "LOW", high_hits, med_hits, low_hits
    

def recommend_action(risk: str) -> str:
    if risk == "HIGH":
        return "Immediate inspection and repair required. Consider shutdown until resolved."
    if risk == "MEDIUM":
        return "Schedule maintenance soon and monitor condition."
    return "No urgent action required. Routine monitoring is sufficient."


def analyze_description(description: str) -> AnalysisResult:
    norm = normalize(description)

    risk, high_hits, med_hits, low_hits = determine_risk(norm)

    summary = build_summary(description)

    action = recommend_action(risk)

    # kleine Ergänzung im Summary mit gefundenen Treffern
    summary_extra = f"\n(keyword hits — high:{high_hits}, medium:{med_hits}, low:{low_hits})"

    return AnalysisResult(
        summary=summary + summary_extra,
        risk_level=risk,
        recommended_action=action
    )


def main():
    # Beispiel-Inspektionsbeschreibung (kann frei geändert werden)
    inspection_text = "Test inspection text"
    result = analyze_description(inspection_text)

    print("\n=== Inspection Analysis ===")
    print("Summary:")
    print(result.summary)

    print("\nDetails:")
    print(result.summary.split("(")[-1].replace(")", ""))

    print("\nRisk level:")
    print(result.risk_level)

    print("\nRecommended action:")
    print(result.recommended_action)
    print("===========================\n")


if __name__ == "__main__":
    main()
