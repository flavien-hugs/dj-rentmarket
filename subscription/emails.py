from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_multiple_email(email, receiver):
    subject = 'Welcome to Laughing Blog Tutorial'
    sender = 'test@achiengcindy.com'

    # passing in the context variable
    text_template = render_to_string(
        'subscribe/email_subscribe.txt', {'email': email})
    html_template = render_to_string(
        'subscribe/email_subscribe.html', {'email': email})
    message = EmailMultiAlternatives(
        subject, text_template, sender, [receiver])

    message.attach_alternative(html_template, 'text/html')
    message.send()
