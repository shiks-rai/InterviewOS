import html
import streamlit as st
import plotly.graph_objects as go
from resume_parser import parse_resume
from interviewer import get_next_question, evaluate_answer, determine_difficulty
from evaluator import generate_scorecard
from feedback import answer_feedback_question
from report_generator import generate_pdf_report

st.set_page_config(
    page_title="InterviewOS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #080d14; color: #e2e8f0; }
header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.upload-hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 48px 24px;
}
.logo-text {
    font-size: 3.6rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.logo-sub {
    color: #475569;
    font-size: 1rem;
    font-weight: 400;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 48px;
}
.upload-card {
    background: #0f1923;
    border: 1px solid #1e2d3d;
    border-radius: 20px;
    padding: 40px;
    width: 100%;
    max-width: 520px;
}
.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 8px;
    margin-top: 24px;
}
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid #1e2d3d;
}
.topbar-brand {
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.topbar-meta { color: #475569; font-size: 0.85rem; }
.progress-wrap { margin-bottom: 28px; }
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #475569;
    margin-bottom: 6px;
}
.progress-track {
    height: 4px;
    background: #1e2d3d;
    border-radius: 2px;
    overflow: hidden;
}
.progress-fill {
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transition: width 0.4s ease;
}
.diff-wrap { margin-bottom: 28px; }
.diff-label { font-size: 0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:#475569; margin-bottom:6px; }
.diff-easy   { display:inline-block; background:#052e16; color:#86efac; border:1px solid #166534; padding:5px 14px; border-radius:6px; font-size:0.82rem; font-weight:600; }
.diff-medium { display:inline-block; background:#1c1003; color:#fde68a; border:1px solid #92400e; padding:5px 14px; border-radius:6px; font-size:0.82rem; font-weight:600; }
.diff-hard   { display:inline-block; background:#1f0505; color:#fca5a5; border:1px solid #7f1d1d; padding:5px 14px; border-radius:6px; font-size:0.82rem; font-weight:600; }
.score-title { font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:#475569; margin-bottom:12px; }
.score-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    background: #0f1923;
    border: 1px solid #1e2d3d;
}
.score-q-label { font-size:0.8rem; color:#64748b; }
.score-high { color:#4ade80; font-weight:700; font-size:0.88rem; }
.score-mid  { color:#fbbf24; font-weight:700; font-size:0.88rem; }
.score-low  { color:#f87171; font-weight:700; font-size:0.88rem; }
.score-bar-wrap { height:3px; background:#1e2d3d; border-radius:2px; margin-top:4px; }
.score-bar-fill { height:3px; border-radius:2px; }
.bubble-interviewer {
    background: #0d1f35;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #3b82f6;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    line-height: 1.7;
}
.bubble-candidate {
    background: #130d24;
    border: 1px solid #2e1f4a;
    border-left: 3px solid #8b5cf6;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    line-height: 1.7;
}
.bubble-role {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.role-interviewer { color: #60a5fa; }
.role-candidate   { color: #a78bfa; }
.score-hero {
    text-align: center;
    padding: 56px 24px 40px;
    border-bottom: 1px solid #1e2d3d;
    margin-bottom: 40px;
}
.score-hero-num {
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -3px;
}
.tag-pill {
    display: inline-block;
    background: #0f1923;
    border: 1px solid #1e2d3d;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #64748b;
    margin: 4px;
}
.section-card {
    background: #0a1120;
    border: 1px solid #1e2d3d;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
}
.section-heading {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 18px;
}
.skill-row { margin-bottom: 14px; }
.skill-name { font-size: 0.85rem; color: #cbd5e1; margin-bottom: 5px; }
.skill-track { height: 5px; background: #1e2d3d; border-radius: 3px; }
.skill-fill-high { height:5px; border-radius:3px; background:linear-gradient(90deg,#22c55e,#4ade80); }
.skill-fill-mid  { height:5px; border-radius:3px; background:linear-gradient(90deg,#f59e0b,#fbbf24); }
.skill-fill-low  { height:5px; border-radius:3px; background:linear-gradient(90deg,#ef4444,#f87171); }
.strength-item { color:#86efac; font-size:0.88rem; padding:6px 0; border-bottom:1px solid #0f1923; line-height:1.5; }
.weakness-item { color:#fca5a5; font-size:0.88rem; padding:6px 0; border-bottom:1px solid #0f1923; line-height:1.5; }
.study-chip {
    display:inline-block;
    background:#0d1f35;
    border:1px solid #1e3a5f;
    color:#93c5fd;
    border-radius:8px;
    padding:8px 14px;
    font-size:0.82rem;
    margin:4px;
}
.feedback-q { color:#93c5fd; font-size:0.9rem; font-weight:600; margin-bottom:6px; }
.feedback-a { color:#cbd5e1; font-size:0.88rem; line-height:1.7; }

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100%;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stSelectbox > div > div, .stFileUploader > div {
    background: #0f1923 !important;
    border-color: #1e2d3d !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
div[data-testid="stChatInput"] > div {
    background: #0f1923 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 12px !important;
}
.stProgress > div > div { background: linear-gradient(90deg,#3b82f6,#8b5cf6) !important; }
div[data-testid="stSelectSlider"] span { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session defaults
defaults = {
    "stage": "upload", "resume_data": None, "messages": [],
    "scores": [], "difficulty": "medium", "question_count": 0,
    "scorecard": None, "last_question": "", "role": "ML Engineer",
    "company": "General", "feedback_history": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

MAX_Q = 8

def esc(t):
    """Make user/AI text safe to drop inside our HTML blocks."""
    return html.escape(str(t)).replace("\n", "<br>")

def score_cls(s):
    return "score-high" if s >= 7 else ("score-mid" if s >= 5 else "score-low")

def skill_fill_cls(s):
    return "skill-fill-high" if s >= 7 else ("skill-fill-mid" if s >= 5 else "skill-fill-low")

def score_color(s):
    return "#4ade80" if s >= 7 else ("#fbbf24" if s >= 5 else "#f87171")


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "upload":
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown("""
        <div class="upload-hero">
            <div class="logo-text">InterviewOS</div>
            <div class="logo-sub">Adaptive AI Interview Simulator</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

        st.markdown('<div class="section-label" style="margin-top:20px;">Role</div>', unsafe_allow_html=True)
        role = st.selectbox("Role", ["ML Engineer", "Data Analyst"], label_visibility="collapsed")

        st.markdown('<div class="section-label" style="margin-top:20px;">Company style</div>', unsafe_allow_html=True)
        company = st.selectbox("Company", ["General", "Google", "Amazon", "Microsoft", "Startup"],
                               label_visibility="collapsed")

        st.markdown('<div class="section-label" style="margin-top:20px;">Starting difficulty</div>', unsafe_allow_html=True)
        difficulty = st.select_slider("Difficulty", ["easy", "medium", "hard"],
                                      value="medium", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        if uploaded_file:
            if st.button("Begin Interview →", use_container_width=True):
                with st.spinner("Reading resume..."):
                    rd = parse_resume(uploaded_file)
                    st.session_state.resume_data = rd
                    st.session_state.role = role
                    st.session_state.company = company
                    st.session_state.difficulty = difficulty
                with st.spinner("Preparing first question..."):
                    fq = get_next_question([], rd, difficulty, role, company)
                st.session_state.messages.append({"role": "assistant", "content": fq})
                st.session_state.last_question = fq
                st.session_state.stage = "interview"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "interview":
    chat_col, side_col = st.columns([3, 1])

    with side_col:
        st.markdown(f"""
        <div style="padding:28px 20px; background:#0a1120; border-left:1px solid #1e2d3d; min-height:100vh;">
            <div style="font-size:1rem;font-weight:800;background:linear-gradient(135deg,#60a5fa,#a78bfa);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;">
                InterviewOS
            </div>
            <div style="color:#475569;font-size:0.78rem;margin-bottom:28px;">
                {st.session_state.role} · {st.session_state.company}
            </div>
        """, unsafe_allow_html=True)

        pct = int((st.session_state.question_count / MAX_Q) * 100)
        st.markdown(f"""
            <div class="progress-wrap">
                <div class="progress-label">
                    <span>Progress</span>
                    <span>{st.session_state.question_count}/{MAX_Q}</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        d = st.session_state.difficulty
        st.markdown(f"""
            <div class="diff-wrap">
                <div class="diff-label">Difficulty</div>
                <div class="diff-{d}">{d.upper()}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.scores:
            st.markdown('<div class="score-title">Answer Scores</div>', unsafe_allow_html=True)
            for i, s in enumerate(st.session_state.scores):
                bar_w = int(s * 10)
                fill_color = "#4ade80" if s >= 7 else ("#fbbf24" if s >= 5 else "#f87171")
                st.markdown(f"""
                <div class="score-row">
                    <div style="width:100%;">
                        <div style="display:flex;justify-content:space-between;">
                            <span class="score-q-label">Q{i+1}</span>
                            <span class="{score_cls(s)}">{s}/10</span>
                        </div>
                        <div class="score-bar-wrap">
                            <div class="score-bar-fill" style="width:{bar_w}%;background:{fill_color};"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with chat_col:
        st.markdown(f"""
        <div style="padding:32px 40px;">
            <div class="topbar">
                <div class="topbar-brand">🎯 InterviewOS</div>
                <div class="topbar-meta">Question {st.session_state.question_count + 1} of {MAX_Q}</div>
            </div>
        """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div class="bubble-interviewer">
                    <div class="bubble-role role-interviewer">🎙 Interviewer</div>
                    {esc(msg['content'])}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bubble-candidate">
                    <div class="bubble-role role-candidate">You</div>
                    {esc(msg['content'])}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.question_count < MAX_Q:
            answer = st.chat_input("Type your answer...")
            if answer:
                st.session_state.messages.append({"role": "user", "content": answer})
                st.session_state.question_count += 1

                with st.spinner(""):
                    ev = evaluate_answer(st.session_state.last_question, answer)
                    score = ev["score"]
                    st.session_state.scores.append(score)
                    new_diff = determine_difficulty(score, st.session_state.difficulty)

                if new_diff != st.session_state.difficulty:
                    st.toast(f"Difficulty → {new_diff.upper()}", icon="⚡")
                st.session_state.difficulty = new_diff

                if st.session_state.question_count >= MAX_Q:
                    st.session_state.stage = "scorecard"
                    st.rerun()
                else:
                    with st.spinner(""):
                        nq = get_next_question(
                            st.session_state.messages,
                            st.session_state.resume_data,
                            st.session_state.difficulty,
                            st.session_state.role,
                            st.session_state.company
                        )
                    st.session_state.messages.append({"role": "assistant", "content": nq})
                    st.session_state.last_question = nq
                    st.rerun()
        else:
            st.session_state.stage = "scorecard"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — SCORECARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "scorecard":

    if st.session_state.scorecard is None:
        with st.spinner("Generating your scorecard..."):
            st.session_state.scorecard = generate_scorecard(
                st.session_state.resume_data,
                st.session_state.messages,
                st.session_state.scores,
                st.session_state.role
            )

    sc = st.session_state.scorecard
    rd = st.session_state.resume_data
    overall = sc["overall_score"]
    hero_color = score_color(overall)

    st.markdown(f"""
    <div class="score-hero">
        <div style="color:#475569;font-size:0.78rem;font-weight:600;letter-spacing:.1em;
                    text-transform:uppercase;margin-bottom:16px;">Interview Complete</div>
        <div class="score-hero-num" style="color:{hero_color};">
            {overall}<span style="font-size:2rem;color:#334155;">/10</span>
        </div>
        <div style="margin-top:16px;">
            <span class="tag-pill">{esc(rd['name'])}</span>
            <span class="tag-pill">{st.session_state.role}</span>
            <span class="tag-pill">{st.session_state.company}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Skill Breakdown</div>', unsafe_allow_html=True)
        for skill, score in sc["skill_scores"].items():
            bar_w = int(score * 10)
            fill = skill_fill_cls(score)
            st.markdown(f"""
            <div class="skill-row">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span class="skill-name">{esc(skill)}</span>
                    <span class="{score_cls(score)}" style="font-size:0.85rem;font-weight:700;">{score}/10</span>
                </div>
                <div class="skill-track">
                    <div class="{fill}" style="width:{bar_w}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        skills = list(sc["skill_scores"].keys())
        values = list(sc["skill_scores"].values())
        fig = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=skills + [skills[0]],
            fill='toself',
            fillcolor='rgba(59,130,246,0.12)',
            line=dict(color='#3b82f6', width=2),
            marker=dict(color='#8b5cf6', size=5)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='#0a1120',
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#1e2d3d',
                                tickfont=dict(color='#334155', size=9)),
                angularaxis=dict(gridcolor='#1e2d3d', tickfont=dict(color='#64748b', size=10))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">✦ Strengths</div>', unsafe_allow_html=True)
        for s in sc["strengths"]:
            st.markdown(f'<div class="strength-item">▸ {esc(s)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">▲ Areas to Improve</div>', unsafe_allow_html=True)
        for w in sc["weaknesses"]:
            st.markdown(f'<div class="weakness-item">▸ {esc(w)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#94a3b8;line-height:1.8;font-size:0.9rem;">{esc(sc["recommendation"])}</p>',
                unsafe_allow_html=True)
    if sc.get("study_topics"):
        st.markdown('<div class="section-heading" style="margin-top:20px;">Study Next</div>',
                    unsafe_allow_html=True)
        chips = "".join([f'<span class="study-chip">{esc(t)}</span>' for t in sc["study_topics"]])
        st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_dl, col_new = st.columns([1, 1])
    with col_dl:
        if st.button("📄 Download PDF Report", use_container_width=True):
            pdf_path = generate_pdf_report(rd, sc, st.session_state.scores,
                                           st.session_state.role, st.session_state.company)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Save Report", data=f,
                                   file_name=f"InterviewOS_{rd['name'].replace(' ', '_')}.pdf",
                                   mime="application/pdf", use_container_width=True)
    with col_new:
        if st.button("🔄 Start New Interview", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown('<div class="section-card" style="margin-top:12px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Ask About Your Performance</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#334155;font-size:0.82rem;margin-bottom:16px;">'
                'e.g. "Why did I score low on SQL?" · "What should I study first?" · "Where did I lose marks?"'
                '</p>', unsafe_allow_html=True)

    for item in st.session_state.feedback_history:
        st.markdown(f'<div class="feedback-q">❓ {esc(item["q"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-a">{esc(item["a"])}</div>', unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#1e2d3d;margin:16px 0;">', unsafe_allow_html=True)

    fq = st.chat_input("Ask anything about your interview...")
    if fq:
        with st.spinner("Analysing..."):
            fa = answer_feedback_question(fq, st.session_state.messages, sc)
        st.session_state.feedback_history.append({"q": fq, "a": fa})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)