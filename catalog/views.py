from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views import View
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.conf import settings
from .services import get_products_by_category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        cache_key = f'product_detail_{product_id}'
        cached_product = cache.get(cache_key)
        if cached_product:
            return cached_product
        product = super().get_object(queryset)
        cache.set(cache_key, product, settings.CACHE_TTL_PRODUCT_DETAIL)
        return product



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return redirect('catalog:product_list')


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.has_perm('catalog.change_product'):
            raise PermissionDenied("Вы не можете редактировать чужой товар")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("Вы не можете удалять чужой товар")
        return super().dispatch(request, *args, **kwargs)


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


class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)
