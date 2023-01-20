from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from app.forms.contact_form import ContactForm


class CreateContactPage(CreateView):
    form_class = ContactForm
    template_name = 'app/contact.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super(CreateContactPage, self).form_valid(form)
        form.save()
        return result

