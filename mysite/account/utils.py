from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],  # Corrected from 'bdy' to 'body'
            from_email=os.environ.get('EMAIL_FROM'),  # Removed the extra period here
            to=[data['to_email']]
        )
        email.send()
