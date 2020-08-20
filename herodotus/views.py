from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'home.html', {})

class AddContentView(TemplateView):
    def get(self, request):
        return render(request, 'addcontent.html', {})