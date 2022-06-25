from unicodedata import category
from django.db import models
from category.models import Category
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=5000, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    images = models.ImageField(upload_to='products/%y/%m/%d')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.name
