import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from prompts import (
    ANALYSIS_PROMPT,
    REPORT_PROMPT
)

load_dotenv()


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=os.getenv("GROQ_MODEL"),
    temperature=0.2
)


def normalize_response(response_content):

    # STRING
    if isinstance(response_content, str):
        return response_content

    # LIST
    if isinstance(response_content, list):

        extracted = []

        for item in response_content:

            if isinstance(item, dict):

                if "text" in item:
                    extracted.append(item["text"])

            else:
                extracted.append(str(item))

        return "\n".join(extracted)

    # DICT
    if isinstance(response_content, dict):

        if "text" in response_content:
            return response_content["text"]

        return str(response_content)

    return str(response_content)


# -----------------------------------
# ANALYSIS AGENT
# -----------------------------------

def analysis_agent(content: str):

    prompt = f"""
{ANALYSIS_PROMPT}

CONTENT:
{content[:10000]}
"""

    response = llm.invoke(prompt)

    return normalize_response(
        response.content
    )


# -----------------------------------
# THREAT EXTRACTION AGENT
# -----------------------------------

def extract_threats_agent(content: str):

    prompt = f"""
You are a cybersecurity threat extraction agent.

Your task:
Identify cybersecurity threats,
attack categories,
vulnerabilities,
malware,
MITRE ATT&CK techniques,
or OWASP Top 10 issues
mentioned or IMPLIED in the content.

IMPORTANT:
You may infer standard cybersecurity threats from:
- OWASP categories
- MITRE techniques
- security advisories
- vulnerability discussions

EXAMPLES:

OWASP Injection
→ sql injection

Broken Authentication
→ credential theft

Security Misconfiguration
→ cloud misconfiguration

Cross Site Scripting
→ xss

Server Side Request Forgery
→ ssrf

RULES:
- Return ONLY comma-separated threat names
- Maximum 20 threats
- NO explanations
- NO numbering
- NO duplicates
- NO hallucinated variants

GOOD OUTPUT:
sql injection,
xss,
csrf,
credential theft,
ssrf,
privilege escalation

If nothing found return:
NONE

CONTENT:
{content[:12000]}
"""

    response = llm.invoke(prompt)

    result = normalize_response(
        response.content
    )

    # CLEAN OUTPUT
    result = result.split(",")

    cleaned = []

    seen = set()

    for item in result:

        item = item.strip().lower()

        if item and item not in seen:

            seen.add(item)

            cleaned.append(item)

    cleaned = cleaned[:20]

    return ",".join(cleaned)

# -----------------------------------
# REPORT GENERATOR AGENT
# -----------------------------------

def report_agent(
    analysis: str,
    threats: list
):

    prompt = f"""
{REPORT_PROMPT}

ANALYSIS:
{analysis}

THREATS:
{threats}

Generate:
- Incident Summary
- Threat Classification
- Severity
- Threats Detected
- Recommended Mitigation
- Confidence Score
- Escalation Advice
"""

    response = llm.invoke(prompt)

    return normalize_response(
        response.content
    )