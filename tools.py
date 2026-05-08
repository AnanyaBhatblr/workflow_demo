import json
import re

with open(
    "knowledge_base/threats.json",
    "r"
) as f:

    THREATS = json.load(f)


def clean_text(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z0-9\\s]",
        " ",
        text
    )

    return text


def search_threats(content):

    content = clean_text(content)

    matches = []

    for threat, details in THREATS.items():

        score = 0

        threat_lower = threat.lower()

        if threat_lower in content:
            score += 5

        indicators = details.get(
            "indicators",
            []
        )

        matched_indicators = []

        for indicator in indicators:

            indicator_lower = indicator.lower()

            if indicator_lower in content:

                score += 2

                matched_indicators.append(
                    indicator
                )

        if score >= 5:

            matches.append({

                "threat": threat,

                "category": details.get(
                    "category"
                ),

                "severity": details.get(
                    "severity"
                ),

                "confidence_score": score,

                "matched_indicators":
                    matched_indicators,

                "description": details.get(
                    "description"
                ),

                "fix": details.get(
                    "fix"
                )
            })

    matches = sorted(
        matches,
        key=lambda x: x[
            "confidence_score"
        ],
        reverse=True
    )

    return matches