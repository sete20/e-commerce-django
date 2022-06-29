from zipapp import create_archive
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart
from .models import cartItem

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = cartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request),)
        cart.save()
    try:
        cart_item = cartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except cartItem.DoesNotExist:
        cart_item = cartItem.objects.create(
            product=product, cart=cart, quantity=1)
        cart_item.save()
    return redirect('cart')


def decrement_product(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=id)
    cart_item = cartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def increment_product(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=id)
    cart_item = cartItem.objects.get(product=product, cart=cart)
    if product.stock > cart_item.quantity + 1:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_product(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=id)
    cart_item = cartItem.objects.get(product=product, cart=cart)
    # return HttpResponse(cart)
    # exit()
    cart_item.delete()
    return redirect('cart')
