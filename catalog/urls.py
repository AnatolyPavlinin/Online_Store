from django.urls import path
from .views import (ProductListView, ContactsPage, ProductDetailView, ProductCreateView,
                    ProductEditView, ProductDeleteView, ProductsByCategoryView)


app_name = 'catalog'

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products-in-category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
]
