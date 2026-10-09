import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_scorecard(resume_data, conversation_history, scores, role="ML Engineer"):
    transcript = ""
    for msg in conversation_history:
        role_label = "Interviewer" if msg["role"] == "assistant" else "Candidate"
        transcript += f"{role_label}: {msg['content']}\n\n"

    avg_score = sum(scores) / len(scores) if scores else 0

    prompt = f"""
You are an expert interview evaluator for {role} roles.

Candidate: {resume_data['name']}
Skills on resume: {', '.join(resume_data['skills'])}
Average answer score: {avg_score:.1f}/10

Full transcript:
{transcript}

Generate a structured evaluation. Return ONLY this JSON:
{{
    "overall_score": <number 1-10, one decimal>,
    "skill_scores": {{
        "<skill tested>": <score 1-10>
    }},
    "strengths": ["<specific strength from their answers>", "<another>", "<another>"],
    "weaknesses": ["<specific gap from their answers>", "<another>", "<another>"],
    "recommendation": "<3 sentence honest assessment with specific next steps>",
    "study_topics": ["<topic1 to study>", "<topic2>", "<topic3>"]
}}

Only include skills actually tested. Be honest — do not inflate scores.
"""

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result = response.choices[0].message.content.strip()
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    return json.loads(result)