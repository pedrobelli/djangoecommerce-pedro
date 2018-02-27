# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product, Category

class ProductListView(generic.ListView):

    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'
    paginate_by = 3

class CategoryListView(generic.ListView):

    context_object_name = 'products'
    template_name = 'catalog/category.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

product_list = ProductListView.as_view()
category = CategoryListView.as_view()

def product(request, slug):
    product = Product.objects.get(slug=slug)
    context = {
        'current_product': product
    }
    return render(request, 'catalog/product.html', context)