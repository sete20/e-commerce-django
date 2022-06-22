from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    # the names which showing in the dahsboard table
    list_display = ('name', 'price', 'stock', 'category',
                    'created_at', 'is_available',)
    # linking the slug with the name column
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
# Register your models here.
