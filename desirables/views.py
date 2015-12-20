from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.

def home_page(request):
    return render_to_response("index.html")

def login_page(request):
    return render_to_response("login.html")
