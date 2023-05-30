from django.core.mail import EmailMessage
from smtplib import SMTPException
import os

class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data['email_subject'],
                body=data['body'],
                from_email=os.environ.get('EMAIL_FROM'),
                to=[data['to_email']]
            )
            # Sending automatic email
            email.send()
        except SMTPException as e:
            # Handle the exception (e.g., log the error, raise an appropriate exception, etc.)
            print(f"Failed to send email: {str(e)}")
            raise
