from . import views
from django.urls import path
urlpatterns = [
    path('', views.store, name='store'),
    path('details/<int:id>', views.details, name='store.details'),
    path('<slug:slug>', views.ProductCategoryGetBySlug,
         name='ProductCategoryGetBySlug')

]
