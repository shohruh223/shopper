from django.forms import ModelForm
from app.models import Product


class ProductModelForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'