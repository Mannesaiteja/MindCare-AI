🧠 MindCare AI
AI-Based Mental Health Assessment & Recommendation System
📌 Project Overview

MindCare AI is an artificial intelligence–based mental health screening system designed to analyze user responses from a structured questionnaire and predict mental health conditions such as Stress, Anxiety, and Depression. The system provides early awareness, personalized recommendations, and a hospital-style clinical report to support mental well-being.

This project is developed as an academic application to demonstrate the responsible use of AI in healthcare and does not replace professional medical diagnosis.

🎯 Objectives

To assess mental health using a questionnaire-based approach

To apply machine learning for mental health classification

To generate personalized recommendations based on analysis

To create hospital-style PDF reports with graphs

To enable real-time email delivery of reports

To promote mental health awareness using ethical AI

🧠 Technologies Used

Programming Language: Python

Web Framework: Streamlit

Machine Learning: Logistic Regression (Scikit-learn)

Data Handling: Pandas

Visualization: Matplotlib

Model Storage: Joblib

PDF Generation: FPDF

Email Service: Gmail SMTP

⚙️ System Features

Interactive mental health questionnaire (20 questions)

AI-based classification (Normal / Mild / Moderate / High)

Stress, Anxiety, and Depression score calculation

Personalized recommendations

Hospital-style PDF report with logo & watermark

Graphical visualization of mental health indicators

Email delivery of the report in real time

🏗️ System Architecture (High-Level)

User fills mental health questionnaire

Responses are preprocessed and analyzed

Machine learning model predicts mental health level

Scores and recommendations are generated

PDF report is created with graphs

Report is downloaded or emailed to the user

▶️ How to Run the Project Locally
Step 1: Install required libraries
pip install -r requirements.txt

Step 2: Run the application
streamlit run mental_health_web_app.py

Step 3: Open in browser
http://localhost:8501

📦 Project Structure
MindCare-AI/
│
├── mental_health_web_app.py
├── mental_health_model.pkl
├── label_encoder.pkl
├── requirements.txt
├── README.md
└── assets/
    └── logo.png

⚠️ Disclaimer

This system is intended only for screening and awareness purposes.
It does not provide medical diagnosis or treatment.
Users are advised to consult qualified mental health professionals when required.

🌍 Future Enhancements

Integration with mobile applications

Multilingual support

Advanced deep learning models

Secure cloud database storage

Therapist referral system

👨‍🎓 Academic Use

This project is developed as part of an academic curriculum to demonstrate the application of Artificial Intelligence and Machine Learning in healthcare.

📜 License

This project is licensed under the MIT License.
