from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/to/cart/<int:id>', views.add_cart, name='add.to.cart'),

    path('decrement/cart/<int:id>', views.decrement_product,
         name='decrement.item.cart'),
    path('increment/cart/<int:id>', views.increment_product,
         name='increment.item.cart'),

    path('remove/cart/item/<int:id>', views.remove_product,
         name='remove.item.cart'),
]
