# InterviewOS – Adaptive AI Mock-Interview Simulator

InterviewOS helps you practise for technical interviews. Upload your resume, pick a role and a company style, and it runs a personalised mock interview that gets harder or easier depending on how well you answer. At the end you get a scored report and can ask follow-up questions about your own performance.

**Live demo:** [add your Streamlit link here]

## How it works

1. **Upload your resume (PDF)** and choose a role (ML Engineer or Data Analyst), a company style (General, Google, Amazon, Microsoft or Startup) and a starting difficulty.
2. **The interview runs for 8 questions.** Each question is built from your own resume, one at a time. Every answer is scored out of 10, and the difficulty moves between easy, medium and hard based on how you did.
3. **You get a scorecard:** overall score, skill-by-skill breakdown with a radar chart, strengths, weaknesses, a recommendation and topics to study next.
4. **Ask about your performance.** A feedback chat answers questions like "Where did I lose marks?" using specific moments from your own transcript.
5. **Download a PDF report** of the results.

## Features

- Resume parsing with PyMuPDF, with the resume details extracted by an LLM
- Questions based on your actual projects and skills, with no repeated topics
- Adaptive difficulty driven by per-answer scoring
- Role-specific and company-specific questioning styles
- Full conversation memory, so follow-up questions make sense in context
- Structured scorecard with Plotly charts
- Transcript-aware feedback chat
- PDF report export

## Project structure

| File | What it does |
|---|---|
| `app.py` | Streamlit interface and interview flow |
| `resume_parser.py` | Reads the PDF and extracts name, skills, projects, experience and education |
| `interviewer.py` | Builds the interviewer prompt, generates questions, scores answers, adjusts difficulty |
| `evaluator.py` | Generates the final scorecard from the full transcript |
| `feedback.py` | Answers follow-up questions about the interview |
| `report_generator.py` | Creates the downloadable PDF report |

## Tech used

- Python
- Streamlit
- OpenAI API (`gpt-5.4-nano`)
- PyMuPDF
- Plotly
- fpdf2
- python-dotenv

## Run it locally

1. Clone the repo
   ```
   git clone https://github.com/<your-username>/InterviewOS.git
   cd InterviewOS
   ```
2. Install the requirements
   ```
   pip install -r requirements.txt
   ```
3. Create a file named `.env` in the project folder and add your own OpenAI API key
   ```
   OPENAI_API_KEY=your_key_here
   ```
4. Start the app
   ```
   streamlit run app.py
   ```

Never commit your `.env` file or your API key. The `.gitignore` in this repo already excludes `.env`.

## Deploying on Streamlit Cloud

Connect this repo on Streamlit Cloud, and add `OPENAI_API_KEY` under the app's **Secrets** settings.

## Author

Shikha Rai, Computer Science Engineering graduate, National Institute of Engineering, Mysuru
