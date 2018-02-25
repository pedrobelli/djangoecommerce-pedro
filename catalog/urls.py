# coding=utf-8

from django.urls import path, re_path
from . import views

app_name='catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    re_path('categorias/(?P<slug>[\w_-]+)/', views.category, name='category'),
    re_path('produtos/(?P<slug>[\w_-]+)/', views.product, name='product'),
]