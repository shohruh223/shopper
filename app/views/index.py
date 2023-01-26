from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from app.forms.product_form import ProductModelForm
from app.models import Product, Category

#sd
# def index(request):
#     products = Product.objects.order_by('-id')
#     context = {
#         'products':products
#     }
#     return render(request, 'app/index.html', context)
# abdulla

class IndexPage(ListView):
    # template_engine = Product.objects.order_by('-id')
    products = Product.objects.order_by('-id')
    categories = Category.objects.filter(parent=None)
    categories_children = Category.objects.filter(parent=True)
    extra_context = {
        "products":products,
        'categories':categories,
        'categories_children':categories_children,
    }
    model = Product
    template_name = 'app/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.request.GET.get('slug', None)
        if slug:
            qs = qs.filter(category__slug=slug)
        return qs

#e2
# def product_details(request, product_id):
#     product = Product.objects.filter(id=product_id).first()
#     context = {
#         'product':product
#     }
#     return render(request, 'app/product_details.html', context)


class ProductDetailsPage(DetailView):
    model = Product
    template_name = 'app/product_details.html'


def shop_view(request):
    return render(request, 'app/shop.html')


def shopping_cart(request):
    return render(request, 'app/shopping_cart.html')


def checkout(request):
    return render(request, 'app/checkout.html')


# def create_product(request):
#     category = Category.objects.all()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return redirect('index')
#     form = ProductModelForm()
#     context = {
#         "form":form,
#         "sizes":Product.ChoiceSize,
#         "colors":Product.ChoiceColor,
#         "categories":category
#     }
#     return render(request, 'app/create_product.html', context)


class CreateProductPage(CreateView):
    category = Category.objects.all()
    form_class = ProductModelForm
    template_name = 'app/create_product.html'
    success_url = reverse_lazy('index')
    extra_context = {"categories":category,
                     "sizes":Product.ChoiceSize,
                     "colors":Product.ChoiceColor}

    def form_valid(self, form):
        result = super(CreateProductPage, self).form_valid(form)
        form.save()
        return result


def update_product(request, product_id):
    category = Category.objects.all()
    product = Product.objects.filter(id=product_id).first()
    if request.method == "POST":
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
        return redirect('index')

    form = ProductModelForm(instance=product)
    context = {
        "form":form,
        "sizes": Product.ChoiceSize,
        "colors": Product.ChoiceColor,
        "categories": category
    }
    return render(request, 'app/update_product.html', context)


# class UpdateProductPage(UpdateView):
#     category = Category.objects.all()
#     form_class = ProductModelForm
#     template_name = 'app/update_product.html'
#     success_url = reverse_lazy('index')
#     extra_context = {"categories":category,
#                      "sizes":Product.ChoiceSize,
#                      "colors":Product.ChoiceColor}
#
#     def form_valid(self, form):
#         result = super(UpdateProductPage, self).form_valid(form)
#         form.save()
#         return result
#
#     def get_queryset(self):
#         queryset = super(UpdateProductPage, self).get_queryset()
#         return queryset.filter(pk=3)


def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product:
        product.delete()
    return redirect('index')




# class DeleteProductPage(DeleteView):
#     form_class = ProductModelForm
#     success_url = reverse_lazy('index')



