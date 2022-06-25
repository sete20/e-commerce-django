from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
# Create your views here.


def store(request):
    context = {
        'products': Product.objects.all().filter(is_available=True),
        'categories': Category.objects.all(),
        'products_count': Product.objects.filter(is_available=True).count()
    }
    return render(request, 'store/store.html', context)


def details(request, id):
    context = {'product': Product.objects.filter(id=id).first(), }
    return render(request, 'store/details.html', context)


def ProductCategoryGetBySlug(request, slug):
    context = {
        'products': Product.objects.filter(category__slug=slug),
        'categories': Category.objects.all(),
        'products_count': Product.objects.filter(is_available=True).count()
    }
    return render(request, 'store/store.html', context)
