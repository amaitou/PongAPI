
from django.core.mail import EmailMessage

class Verification:

    @staticmethod
    def send_verification_email(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['email']])
        email.send()