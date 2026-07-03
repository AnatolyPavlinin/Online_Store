from django.shortcuts import redirect
from django.urls import resolve

class AdminAccessMiddleware:
    """Средство защиты административных страниц"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = ['home', 'product_detail', 'login', 'register']
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        current_route = resolve(request.path).url_name

        if current_route not in public_urls and not request.user.is_authenticated:
            return redirect('users:login')

        response = self.get_response(request)
        return response
