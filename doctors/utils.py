from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


#Email sending helper function
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user' : user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    destination_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[destination_email])
    mail.send()


#Admin approval helper function
def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    destination_email = context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[destination_email])
    mail.send()
    