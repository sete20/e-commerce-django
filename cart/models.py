from django.db import models
from store.models import Product
from store.models import Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class cartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)

    def __str__(self):
        return self.product

    def sub_total(self):
        return self.quantity * self.product.price

    def __unicode__(self):
        return self.product
