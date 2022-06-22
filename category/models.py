from distutils.command.upload import upload
from pickle import TRUE
from django.db import models
from numpy import imag

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='photos/categories/%y/%m/%d', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
