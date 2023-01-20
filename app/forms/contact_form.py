from django import forms

from app.models import Contact


class ContactForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Contact
        # fields = ('subject', 'message')
        exclude = ()

