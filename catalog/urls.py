from django.urls import path
from .views import ProductListView, ContactsPage, ProductDetailView


app_name = 'catalog'

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
