from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from disk.models import Project, Version
from django.http import JsonResponse
from django.conf import settings

import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

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
                return HttpResponseRedirect('/disk/')
            else:
                #return HttpResponseRedirect('/login/')
                return HttpResponseRedirect('')
    return render(request, 'signin.html')

def sign_out(request):
    logout(request)
    return render_to_response('home.html')

def sign_up(request):
    if request.POST:
        userName = request.POST['userName']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username = userName, email=email, password=password)
        return HttpResponseRedirect('/disk/')
    return render(request, 'signup.html')

def deleteVersion(request, version_id):
    Version.objects.filter(id=version_id).delete()

def deleteProject(request, project_id):
    Version.objects.filter(project_id=project_id).delete()
    Project.objects.filter(id=project_id).delete()
    return HttpResponseRedirect('/disk/')

def searchKeyword(request):
    if request.GET:
        keyword = request.GET['keyword']
        jResult = []
        ix = open_dir(os.path.join(settings.BASE_DIR, 'static', 'media', 'index'))
        searcher = ix.searcher()
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(keyword)
            results = searcher.search(query)
            for hit in results:
                stc = hit['stc'].replace('\n','')
                str = {'path': hit['path'] , 'stc': stc}
                jResult.append(str)
        response = JsonResponse(jResult, safe=False)
        return response