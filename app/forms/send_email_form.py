from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from app.models import User
from app.views.token import account_activation_token
from root.settings import EMAIL_HOST_USER


def send_email(email, request, _type):

    user = User.objects.get(email=email)
    subject = 'Activate your account'
    current_site = get_current_site(request)
    message = render_to_string('app/auth/activation_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
        'token': account_activation_token.make_token(user),
    })

    from_email = EMAIL_HOST_USER
    recipient_list = [email]

    result = send_mail(subject, message, from_email, recipient_list)
    print('Send to MAIL')