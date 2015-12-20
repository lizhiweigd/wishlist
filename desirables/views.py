from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import render_to_response

from django.template.context_processors import csrf

from django.contrib.auth import authenticate, login

# Create your views here.

def home_page(request):
    return render_to_response("index.html")

def login_page(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", c)

def login(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Can only log in with POST.")

    if "username" not in request.POST:
        return HttpResponseBadRequest("username parameter required for login.")

    if "password" not in request.POST:
        return HttpResponseBadRequest("password parameter required for login.")

    user = authenticate(username=request.POST["username"], password=request.POST["password"])
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/main")
        else:
            return HttpResponseRedirect("/disabled_login")
    else:
        return HttpResponseRedirect("/invalid_login")
