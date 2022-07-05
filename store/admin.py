from django.contrib import admin

from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    # the names which showing in the dahsboard table
    list_display = ('price', 'stock', 'category',
                    'created_at', 'is_available',)
    # linking the slug with the name column
    prepopulated_fields = {'slug': ('name',)}


class VariationAdmin(admin.ModelAdmin):
    # the names which showing in the dahsboard table
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Variation, VariationAdmin)

# Register your models here.
