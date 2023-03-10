from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import Form, EmailField, CharField
from app.models import User


class LoginForm(AuthenticationForm):
    username = CharField(required=False)
    email = EmailField()
    password = CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email not found')
        return email

    def clean_password(self):
        email = self.data.get('email')
        password = self.data.get('password')

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise ValidationError('This password not found')
        return password

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(Form):
    email = EmailField()
    password = CharField(max_length=155)
    confirm_password = CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is wrong')
        return password

    @atomic
    def save(self):
        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            is_active=False
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()


class ForgotPasswordForm(Form):
    email = EmailField()

    # def send_email(self):
    #     email = self.cleaned_data.get('email')
    #     subject = 'xabar'
    #     message = 'qanaqadir xabar'
    #     from_email = EMAIL_HOST_USER
    #     recipient_list = [email]
    #     result = send_mail(subject, message, from_email, recipient_list)
    #     print(result)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email is not registered')
        return email