from django.urls import path

from . import views

urlpatterns = [
    path('<str:catalog_slug>/', views.item, name='catalog'),
    path('product/<str:product_slug>/', views.item_in_detail, name='product'),
]
