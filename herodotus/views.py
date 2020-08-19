from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

class HomeView(TemplateView):
    def get(self, request):
        response = render(request, 'home.html', {})
        return response