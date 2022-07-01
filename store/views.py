from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
# Create your views here.
from cart.views import _cart_id
from cart.models import cartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def store(request):

    products = Product.objects.all().filter(is_available=True).order_by('id')
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 1)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': Category.objects.all(),

    }
    return render(request, 'store/store.html', context)


def details(request, id):

    product = Product.objects.filter(id=id).first()
    context = {
        'product': product,
        'in_cart': cartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    }
    return render(request, 'store/details.html', context)


def ProductCategoryGetBySlug(request, slug):

    products = Product.objects.all().filter(
        is_available=True, category__slug=slug).order_by('id')
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 1)
    paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {

        'products': paged_products,
        'product_count': product_count,
        'categories': Category.objects.all(),

    }
    return render(request, 'store/store.html', context)


def search(request):

    if 'q' in request.GET:
        q = request.GET.get('q')
        products = Product.objects.order_by(
            '-created_at').filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(slug__icontains=q))
        product_count = products.count()
    context = {
        'products': products,
        'q': q,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context=context)
