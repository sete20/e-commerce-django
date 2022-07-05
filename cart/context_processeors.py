from urllib import request

from django.http import HttpResponse
from .models import Cart, cartItem
from .views import _cart_id


def cart_quantity(request):
    quantity = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = cartItem.objects.filter(cart=cart)
            cart_count = sum([cart_item.quantity for cart_item in cart_items])
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
