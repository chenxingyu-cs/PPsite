from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def home(request):
    context = {}
    template = 'home.html'
    return render(request, template, context)

def sign_in(request):
    if request.POST:
        userName = request.POST['userName']
        password = request.POST['password']
        user = authenticate(username=userName, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # return HttpResponseRedirect('/disk/')
                return HttpResponse('Sign in success!')
            else:
                #return HttpResponseRedirect('/login/')
                return HttpResponseRedirect('')
    return render(request, 'signin.html')

def sign_out(request):
    logout(request)
    return render('home.html')

