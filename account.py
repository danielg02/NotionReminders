import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Account:
    def __init__(self, email, pas=None):
        self.email = email
        self.pas = pas
        self.smtp = "smtp.gmail.com"
        self.port = 587


    def send_email(self, receiver, reminder_msg, event_time):
        server = smtplib.SMTP(self.smtp, self.port)
        server.starttls()
        server.login(self.email, self.pas)

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = receiver.email

        msg['Subject'] = f"UPCOMING TASK"
        body = f"Upcoming tasks: {reminder_msg}\nMessage sent at: {event_time}\n\nThis is an automated email. Please don't reply."
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        server.sendmail(self.email, receiver.email, sms)
        server.quit()

