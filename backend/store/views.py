from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.shortcuts import render

from .models import Product


def home_view(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "store/home.html", {"products": products})


def search_products(request):
    q = (request.GET.get("q") or "").strip()
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = (request.GET.get("sort") or "").strip()

    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except (InvalidOperation, ValueError):
            pass

    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "name_asc": "name",
        "name_desc": "-name",
        "newest": "-created_at",
    }
    ordering = sort_map.get(sort, "-created_at")
    products = products.order_by(ordering)

    return render(request, "store/partials/product_grid.html", {"products": products})