import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_system_prompt(resume_data, difficulty="medium", role="ML Engineer", company="General"):
    role_instructions = {
        "ML Engineer": """
Focus on: model architecture, training pipelines, evaluation metrics, overfitting/underfitting,
feature engineering, deployment, MLOps, Python/Scikit-learn/PyTorch, data preprocessing,
cross-validation, hyperparameter tuning, production ML systems.
""",
        "Data Analyst": """
Focus on: SQL queries, joins, aggregations, window functions, data cleaning, EDA,
business metrics, dashboard design, statistical analysis, A/B testing, Python/Pandas,
data storytelling, KPIs, Power BI / Tableau.
"""
    }

    company_instructions = {
        "Google": "Ask structured, algorithmic-style questions. Expect depth and edge cases.",
        "Amazon": "Frame questions around real business impact and scale. Use STAR method expectations.",
        "Microsoft": "Balance theoretical knowledge with practical implementation.",
        "Startup": "Focus on breadth, speed, and practical hands-on skills over theory.",
        "General": "Ask balanced technical questions suitable for most companies."
    }

    return f"""
You are a strict but fair technical interviewer at {company}.

Candidate profile:
- Name: {resume_data['name']}
- Skills: {', '.join(resume_data['skills'])}
- Projects: {', '.join(resume_data['projects'])}
- Experience: {resume_data['experience']}
- Education: {resume_data['education']}

Role being interviewed for: {role}
{role_instructions.get(role, role_instructions['ML Engineer'])}

Company style: {company_instructions.get(company, company_instructions['General'])}

Current difficulty: {difficulty.upper()}

Rules:
1. Ask ONE question at a time
2. Base questions on their actual resume — reference specific projects and skills
3. Never repeat a topic already covered in the conversation
4. Do NOT evaluate their answer out loud
5. Do NOT give hints
6. Match difficulty to the current level: easy=conceptual, medium=applied, hard=deep/edge cases
7. Be concise and professional

Begin with a brief one-line greeting and your first question.
"""


def evaluate_answer(question, answer):
    prompt = f"""
You are evaluating a technical interview answer.

Question: {question}
Answer: {answer}

Score from 1-10 based on technical accuracy and depth.
If the candidate says they don't know, refused to answer, or gave an irrelevant response, score it 1-2.

Return ONLY this JSON, nothing else:
{{"score": <number 1-10>, "assessment": "<one sentence reason>"}}
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


def get_next_question(messages, resume_data, difficulty, role="ML Engineer", company="General"):
    system = build_system_prompt(resume_data, difficulty, role, company)
    full_messages = [{"role": "system", "content": system}] + messages

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=full_messages,
        temperature=0.7
    )
    return response.choices[0].message.content


def determine_difficulty(score, current_difficulty):
    if score >= 7:
        if current_difficulty == "easy":
            return "medium"
        elif current_difficulty == "medium":
            return "hard"
        else:
            return "hard"
    elif score <= 4:
        if current_difficulty == "hard":
            return "medium"
        elif current_difficulty == "medium":
            return "easy"
        else:
            return "easy"
    else:
        return current_difficulty