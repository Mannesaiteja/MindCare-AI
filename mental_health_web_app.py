import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import uuid
from datetime import datetime
import smtplib
from email.message import EmailMessage

# ================= EMAIL CONFIG =================
SENDER_EMAIL = "mentalhealth.project1911@gmail.com"
SENDER_PASSWORD = "dobbeadjftcdfwgw"  # Gmail App Password

# ================= LOAD MODEL =================
model = joblib.load("mental_health_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="MindCare AI – Mental Health Assessment System",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 MindCare AI")
st.caption("Smart Technology. Compassionate Care.")
st.markdown(
    "**Disclaimer:** This AI-based system provides screening-level guidance only "
    "and does not replace professional medical diagnosis."
)

# ================= SESSION STATE =================
if "label" not in st.session_state:
    st.session_state.label = None
    st.session_state.stress = 0
    st.session_state.anxiety = 0
    st.session_state.depression = 0
    st.session_state.recs = []

# ================= QUESTIONS =================
questions = [
    "Feeling overwhelmed by daily responsibilities",
    "Difficulty relaxing during free time",
    "Pressure from expectations of others",
    "Mental exhaustion at the end of the day",
    "Increased irritability or frustration",
    "Feeling nervous or anxious without clear reason",
    "Excessive worry about future events",
    "Difficulty concentrating due to worrying thoughts",
    "Restlessness or inability to stay still",
    "Sudden fear or panic in certain situations",
    "Persistent feelings of sadness or low mood",
    "Loss of interest in previously enjoyed activities",
    "Constant tiredness or lack of energy",
    "Feelings of worthlessness or guilt",
    "Sleep disturbances",
    "Feeling emotionally disconnected from others",
    "Avoiding social interactions",
    "Feeling supported by friends or family",
    "Confidence in handling emotional challenges",
    "Hopefulness about the future"
]

scale = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

responses = []

# ================= QUESTIONNAIRE =================
st.subheader("📋 Mental Health Questionnaire")
for i, q in enumerate(questions):
    ans = st.radio(f"Q{i+1}. {q}", list(scale.keys()), key=f"q{i}")
    responses.append(scale[ans])

# ================= HELPER FUNCTIONS =================
def clean_text(text):
    return (
        text.replace("–", "-")
            .replace("—", "-")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .encode("latin-1", "ignore")
            .decode("latin-1")
    )

def clinical_interpretation(label):
    if label == "Normal":
        return "The assessment indicates stable mental well-being with no significant psychological distress."
    elif label == "Mild":
        return "The assessment indicates mild psychological stress that may benefit from early lifestyle interventions."
    elif label == "Moderate":
        return "The assessment indicates moderate mental health strain requiring proactive stress management."
    else:
        return "The assessment indicates high psychological distress and professional consultation is strongly advised."

def next_steps(label):
    if label in ["Normal", "Mild"]:
        return [
            "Maintain a healthy daily routine and sleep schedule.",
            "Engage in regular physical and mindfulness activities.",
            "Repeat the assessment periodically for self-monitoring."
        ]
    else:
        return [
            "Seek consultation with a qualified mental health professional.",
            "Avoid prolonged isolation and maintain social support.",
            "Seek immediate help if symptoms worsen."
        ]

def get_recommendations(label, stress, anxiety, depression):
    recs = []

    if label == "Normal":
        recs += [
            "Maintain a balanced daily routine.",
            "Continue engaging in hobbies and physical activities."
        ]
    elif label == "Mild":
        recs += [
            "Practice meditation for 10–15 minutes daily.",
            "Improve sleep hygiene and reduce screen exposure."
        ]
    elif label == "Moderate":
        recs += [
            "Follow structured stress-management techniques.",
            "Consider professional counseling services."
        ]
    else:
        recs += [
            "Seek immediate consultation with a mental health professional.",
            "Ensure continuous emotional and social support."
        ]

    if stress >= 11:
        recs.append("High stress detected: prioritize rest and workload management.")
    if anxiety >= 11:
        recs.append("High anxiety detected: practice breathing and grounding exercises.")
    if depression >= 11:
        recs.append("High depression indicators detected: professional support is strongly recommended.")

    return recs

def generate_chart(stress, anxiety, depression):
    plt.figure(figsize=(4, 3))
    plt.bar(["Stress", "Anxiety", "Depression"], [stress, anxiety, depression])
    plt.ylim(0, 15)
    plt.ylabel("Score")
    plt.title("Mental Health Indicator Levels")
    plt.tight_layout()
    path = "temp_chart.png"
    plt.savefig(path)
    plt.close()
    return path

# ================= PDF GENERATOR =================
def generate_pdf(label, stress, anxiety, depression, recs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_text_color(220, 220, 220)
    pdf.set_font("Arial", "B", 40)
    pdf.rotate(45)
    pdf.text(30, 190, "CONFIDENTIAL")
    pdf.rotate(0)
    pdf.set_text_color(0, 0, 0)

    if os.path.exists("assets/mindcare_logo.png"):
        pdf.image("assets/mindcare_logo.png", 10, 8, 25)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text("MindCare AI – Mental Health Assessment Report"), ln=True, align="C")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, clean_text("Hospital-Style Psychological Screening"), ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Patient ID: {str(uuid.uuid4())[:8]}", ln=True)
    pdf.cell(0, 7, f"Generated On: {datetime.now().strftime('%d %b %Y, %I:%M %p')}", ln=True)

    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Clinical Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Mental Health Status: {label.upper()}", ln=True)

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Clinical Interpretation", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, clean_text(clinical_interpretation(label)))

    pdf.ln(3)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 8, "Indicator", border=1)
    pdf.cell(60, 8, "Score", border=1, ln=True)
    pdf.set_font("Arial", "", 12)
    for name, val in [("Stress", stress), ("Anxiety", anxiety), ("Depression", depression)]:
        pdf.cell(60, 8, name, border=1)
        pdf.cell(60, 8, f"{val} / 15", border=1, ln=True)

    pdf.ln(5)
    chart = generate_chart(stress, anxiety, depression)
    pdf.image(chart, x=40, w=120)
    os.remove(chart)

    pdf.ln(2)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 6, "Figure 1: Comparative visualization of mental health indicators.")

    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Personalized Recommendations", ln=True)
    pdf.set_font("Arial", "", 12)
    for r in recs:
        pdf.multi_cell(0, 7, clean_text(f"- {r}"))

    pdf.ln(3)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Recommended Next Steps", ln=True)
    pdf.set_font("Arial", "", 12)
    for step in next_steps(label):
        pdf.multi_cell(0, 7, clean_text(f"- {step}"))

    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 6, "Disclaimer: This report is generated by an AI-based screening system and is not a medical diagnosis.")

    return pdf.output(dest="S").encode("latin-1")

# ================= EMAIL FUNCTION =================
def send_email(to_email, pdf_bytes):
    msg = EmailMessage()
    msg["Subject"] = "MindCare AI – Mental Health Analysis Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content("Please find attached your mental health analysis report generated by MindCare AI.")

    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename="MindCare_AI_Report.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# ================= ANALYSIS =================
if st.button("🔍 Analyze & Generate Report"):
    for i in [17, 18, 19]:
        responses[i] = 3 - responses[i]

    stress = sum(responses[0:5])
    anxiety = sum(responses[5:10])
    depression = sum(responses[10:15])

    df = pd.DataFrame([responses], columns=[f"Q{i}" for i in range(1, 21)])
    pred = model.predict(df)

    st.session_state.label = label_encoder.inverse_transform(pred)[0]
    st.session_state.stress = stress
    st.session_state.anxiety = anxiety
    st.session_state.depression = depression
    st.session_state.recs = get_recommendations(
        st.session_state.label, stress, anxiety, depression
    )

    st.success(f"Predicted Mental Health Level: {st.session_state.label}")

# ================= RESULTS =================
if st.session_state.recs:
    pdf = generate_pdf(
        st.session_state.label,
        st.session_state.stress,
        st.session_state.anxiety,
        st.session_state.depression,
        st.session_state.recs
    )

    st.download_button(
        "📥 Download Final Clinical Report (PDF)",
        data=pdf,
        file_name="MindCare_AI_Report.pdf"
    )

    email = st.text_input("📧 Enter email address to receive report")
    if st.button("📨 Send Report via Email"):
        send_email(email, pdf)
        st.success("✅ Email sent successfully with PDF report attached")
