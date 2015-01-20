from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says click <a href=""/rango/about/"">ABOUT</a>!")

def about(request):
    return HttpResponse("Rango says click <a href=""/rango/"">HOME</a>!")
