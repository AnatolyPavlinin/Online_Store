from django.db.models import QuerySet
from .models import Product, Category
from django.conf import settings
from django.core.cache import cache

def get_products_by_category(category_id: int) -> QuerySet:
    """Возвращает активные продукты в указанной категории"""

    cache_key = f'category_{category_id}_list'

    cached_products = cache.get(cache_key)
    if cached_products:
        return cached_products

    products = Product.objects.filter(
        category_id=category_id,
        status='published'
    ).order_by('-created_at')

    cache.set(cache_key, products, settings.CACHE_TTL_CATEGORY_LIST)
    return products
