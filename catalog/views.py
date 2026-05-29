from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return  render(request, 'catalog/home.html', context)

def contacts(request):
    return render(request,'catalog/contacts.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо {name}! Сообщение получено.")
    return  render(request, 'catalog/contacts.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)

