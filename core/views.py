# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView

from .forms import ContactForm

# class IndexView(View):

#     def get(self, request):
#         return render(request, 'index.html')

class IndexView(TemplateView):

    template_name = 'index.html'

index = IndexView.as_view()

def contact(request):
    success = False

    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_email()
        success = True
        
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)
