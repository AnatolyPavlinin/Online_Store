from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views import View
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


class ContactsPage(View):
    template_name = 'catalog/contacts.html'

    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.", status=200)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = 'catalog.can_unpublish_product'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['product_id'])
        product.status = 'hidden'
        product.save()
        return reverse('catalog:product_list')