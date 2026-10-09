import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def answer_feedback_question(question, conversation_history, scorecard):
    transcript = ""
    for msg in conversation_history:
        role = "Interviewer" if msg["role"] == "assistant" else "Candidate"
        transcript += f"{role}: {msg['content']}\n\n"

    system_prompt = f"""
You are an interview coach reviewing a completed interview.

Full transcript:
{transcript}

Scorecard summary:
- Overall: {scorecard['overall_score']}/10
- Skills: {scorecard['skill_scores']}
- Strengths: {scorecard['strengths']}
- Weaknesses: {scorecard['weaknesses']}
- Study topics: {scorecard.get('study_topics', [])}

Answer the candidate's question by referencing specific moments from their transcript.
Never give generic advice. Always say things like "In your answer to the question about X, you said Y — 
which showed..." Be direct, honest, and helpful.
"""

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content