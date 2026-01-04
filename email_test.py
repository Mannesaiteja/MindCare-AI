import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "mentalhealth.project1911@gmail.com"
SENDER_PASSWORD = "dobbeadjftcdfwgw"   # app password (no spaces)

msg = EmailMessage()
msg["Subject"] = "SMTP Test"
msg["From"] = SENDER_EMAIL
msg["To"] = "mentalhealth.project1911@gmail.com"   # put YOUR gmail here
msg.set_content("If you see this email, SMTP is working.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)

print("Email sent successfully")
