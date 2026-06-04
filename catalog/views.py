from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.views.generic import ListView, DetailView
from django.views import View


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsPage(View):
    template_name = 'catalog/contacts.html'

    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.", status=200)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
