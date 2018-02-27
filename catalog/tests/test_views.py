# coding utf-8

from django.test import TestCase, Client
from django.urls import reverse
from model_mommy import mommy
from catalog.models import Category, Product

class ProductListTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('catalog:product_list')
        self.products = mommy.make('catalog.Product', _quantity=10)

    def tearDown(self):
        Product.objects.all().delete()
    
    def test_index_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_context_has_products(self):
        response = self.client.get(self.url)
        self.assertTrue('products' in response.context)

    def test_context_products_per_page(self):
        response = self.client.get(self.url)
        products = response.context['products']
        self.assertEquals(products.count(), 3)

    def test_contextwith_paginator(self):
        response = self.client.get(self.url)
        paginator = response.context['paginator']
        self.assertEquals(paginator.num_pages, 4)
    
    def test_page_not_found(self):
        response = self.client.get('{}?page=5'.format(self.url))
        self.assertEquals(response.status_code, 404)

class CategoryTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = mommy.make('catalog.Category', name='Testando Categoria', slug='testando')
        self.products = mommy.make('catalog.Product', category=self.category, _quantity=15)
        self.url = self.category.get_absolute_url()

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
    
    def test_index_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/category.html')

    def test_context(self):
        response = self.client.get(self.url)
        self.assertTrue('current_category' in response.context)
        current_category = response.context['current_category']
        self.assertEquals(current_category.name, 'Testando Categoria')
        self.assertTrue('products' in response.context)
        products = response.context['products']
        self.assertEquals(products.count(), 3)
