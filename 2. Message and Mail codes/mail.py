import smtplib

HOST = "smtp.office365.com"
PORT = 587

FROM_EMAIL = "xxxx"
TO_EMAIL = "xxxx"
PASSWORD = "xxxx"

MESSAGE = """Subject: Intrusion Detection!!!

Someone intruded through your raspberry pi network. Hurry up!
"""

smtp = smtplib.SMTP(HOST, PORT)

status_code, response = smtp.ehlo()
print(f"[*] Echoing the server: {status_code} {response}")

status_code, response = smtp.starttls()
print(f"[*] Starting TLS connection: {status_code} {response}")

status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
print(f"[*] Logging in: {status_code} {response}")

smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
smtp.quit()
