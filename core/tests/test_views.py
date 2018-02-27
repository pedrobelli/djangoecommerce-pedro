# coding utf-8

from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def tearDown(self):
        pass
    
    def test_index_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_user(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

class ContactViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
    
    def test_index_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_form_ok_success(self):
        data = {'name': 'Pedro', 'email': 'pedro.belli@gmail.com', 'message': 'Teste de envio!'}
        response = self.client.post(self.url, data)
        self.assertTrue(response.context['success'])

    def test_form_ok_sent_email(self):
        data = {'name': 'Pedro', 'email': 'pedro.belli@gmail.com', 'message': 'Teste de envio!'}
        response = self.client.post(self.url, data)
        self.assertEquals(len(mail.outbox), 1)

    def test_form_ok_subject(self):
        data = {'name': 'Pedro', 'email': 'pedro.belli@gmail.com', 'message': 'Teste de envio!'}
        response = self.client.post(self.url, data)
        self.assertEquals(mail.outbox[0].subject, 'Contato do Django E-Commerce')

    def test_form_error(self):
        data = {'name': '', 'email': '', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')
        