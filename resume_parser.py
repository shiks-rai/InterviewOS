import fitz  # this is PyMuPDF
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads your API key from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_file):
    """Takes the uploaded PDF and extracts all raw text from it"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def parse_resume(pdf_file):
    """Sends raw resume text to OpenAI and gets back structured data"""
    raw_text = extract_text_from_pdf(pdf_file)

    prompt = f"""
    You are a resume parser. Extract information from this resume and return ONLY a JSON object.
    No explanation, no extra text, just the JSON.

    Extract these fields:
    - name: candidate's full name
    - skills: list of technical skills
    - projects: list of project names
    - experience: list of work experience descriptions
    - education: highest education qualification

    Resume text:
    {raw_text}

    Return format (strictly follow this):
    {{
        "name": "...",
        "skills": ["skill1", "skill2"],
        "projects": ["project1", "project2"],
        "experience": ["experience1", "experience2"],
        "education": "..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0  # 0 means more consistent, structured output
    )

    result = response.choices[0].message.content.strip()

    # Clean up in case OpenAI wraps it in markdown code blocks
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]

    return json.loads(result)