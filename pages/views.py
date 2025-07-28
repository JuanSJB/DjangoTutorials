from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django import forms
from django.shortcuts import render, redirect

# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
    })
    return context

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

from django.views import View
from django.shortcuts import render

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 599},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 49},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 199}
    ]
    next_id = 5

    @classmethod
    def add_product(cls, name, price, description="No description"):
        new_product = {
            "id": str(cls.next_id),
            "name": name,
            "description": description,
            "price": price
        }
        cls.products.append(new_product)
        cls.next_id += 1


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))  # 🔁 Redirección si ID inválido

        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    description = forms.CharField(required=False)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {
            "title": "Create product",
            "form": form
        })

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            description = form.cleaned_data.get('description', "No description")
            Product.add_product(name, price, description)
            return render(request, 'products/created.html', {"title": "Product Created"})
        else:
            return render(request, self.template_name, {
                "title": "Create product",
                "form": form
            })
