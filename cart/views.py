from zipapp import create_archive
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from .models import Cart
from .models import cartItem
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = cartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = cartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2 / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    print(request.user)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total if "tax" in locals() else 0,
    }
    return render(request, 'store/cart.html', context=context)


def add_cart(request, id):
    current_user = request.user
    product = Product.objects.get(id=id)    # Get object product
    if current_user.is_authenticated:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass

        is_exists_cart_item = cartItem.objects.filter(
            product=product, user=current_user).exists()
        if is_exists_cart_item:
            cart_items = cartItem.objects.filter(
                product=product,
                user=current_user
            )
            existing_variation_list = [
                list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                idex = existing_variation_list.index(product_variations)
                cart_item = cartItem.objects.get(id=id[idex])
                cart_item.quantity += 1
            else:
                cart_item = cartItem.objects.create(
                    product=product,
                    user=current_user,
                    quantity=1
                )
        else:
            cart_item = cartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
        cart_item.save()
        return redirect('cart')
    else:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        try:
            # Get cart using the _cart_id
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_exists_cart_item = cartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_items = cartItem.objects.filter(
                product=product,
                cart=cart
            )
            existing_variation_list = [
                list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                idex = existing_variation_list.index(product_variations)
                cart_item = cartItem.objects.get(id=id[idex])
                cart_item.quantity += 1
            else:
                cart_item = cartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=1
                )
        else:
            cart_item = cartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
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
