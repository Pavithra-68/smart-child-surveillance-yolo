import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import cv2
import os
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

class AlertSystem:
    def __init__(self):
        # 2. Setup Twilio
        self.client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        
        # 3. Setup Email Credentials from .env
        self.EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') # Your 16-char App Password
        self.EMAIL_RECEIVER = os.getenv('TARGET_EMAIL') or self.EMAIL_SENDER # Default to self

    def send_sms_alert(self):
        try:
            message = self.client.messages.create(
                body="⚠️ ALERT: Child in Danger Zone!",
                from_=os.getenv('TWILIO_PHONE'),
                to=os.getenv('TARGET_PHONE')
            )
            print("SMS Sent!")
        except Exception as e:
            print(f"Twilio SMS Error: {e}")

    def send_whatsapp_alert(self):
        try:
            message = self.client.messages.create(
                from_='whatsapp:+14155238886', 
                body="⚠️ GUARDIAN AI: Child detected in Danger Zone!",
                to=f"whatsapp:{os.getenv('TARGET_PHONE')}"
            )
            print(f"WhatsApp Alert Sent! ID: {message.sid}")
        except Exception as e:
            print(f"WhatsApp Error: {e}")

    def send_email_with_photo(self, frame):
        try:
            # Save the danger frame temporarily
            photo_path = "danger_event.jpg"
            cv2.imwrite(photo_path, frame)

            msg = EmailMessage()
            msg['Subject'] = "🔴 EMERGENCY: Child Safety Alert"
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = self.EMAIL_RECEIVER
            msg.set_content("A child has entered the restricted danger zone. See attached photo.")

            # Attach the photo
            with open(photo_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename="danger.jpg")

            # 4. Login and Send using the variables we loaded in __init__
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                smtp.send_message(msg)
            print("Email Sent successfully!")
        except Exception as e:
            # This will now tell you if it's a login error or something else
            print(f"Email Failed: {e}")