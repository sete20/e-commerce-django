from . import views
from django.urls import path
urlpatterns = [
    path('', views.store, name='store'),
    path('product/details/<int:id>', views.details, name='store.details'),
    path('category/<slug:slug>', views.ProductCategoryGetBySlug,
         name='ProductCategoryGetBySlug'),
    path('search', views.search,
         name='search'),


]
