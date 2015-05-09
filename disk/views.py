#coding=utf-8
import datetime
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from disk.models import Project, Version

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import * 


class VersionForm(forms.Form):
    head_img = forms.FileField()

@login_required
def index(request):
    u = request.user
    latest_project_list = Project.objects.filter(user_id=u.id).order_by('-pub_date')
    context =  {'latest_project_list': latest_project_list, 'u':u}
    return render(request, 'index.html', context)

@login_required
def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        uf = VersionForm(request.POST, request.FILES)
        if uf.is_valid():
            if request.FILES['head_img'].name[-4:] == '.pdf':
                head_img = uf.cleaned_data['head_img']
                upload_date = datetime.datetime.now()
                version_name = request.FILES['head_img'].name[:-4]
                version_name += upload_date.strftime('(%Y-%m-%d %H.%M.%S)')
                request.FILES['head_img'].name = version_name + '.pdf'
                new_version = Version(project_id = project_id, upload_date=upload_date, head_img = head_img,
                    version_name = version_name)
                new_version.save()
                project.mod_date = upload_date
                project.save()
            else:
                return HttpResponse('Wrong fomat!!!')
    else:
        uf = VersionForm()
    return render(request, 'detail.html', {'project': project, 'uf':uf})

@login_required
def createProject(request):
    if request.POST:
        user_id = request.user.id
        project_name = request.POST['projectName']
        if project_name != '':
            pub_date = datetime.datetime.now()
            mod_date = pub_date
            new_project = Project(user_id = user_id, project_name = project_name, pub_date = pub_date, mod_date = mod_date)
            new_project.save()
        else:
            return HttpResponseRedirect('/disk/')
    ctx ={}
    ctx.update(csrf(request))
    return HttpResponseRedirect('/disk/')

@login_required
def instruction(request, project_id, version_id):
    currentVersion = Version.objects.get(id=version_id)
    file_path = currentVersion.head_img
    a = ''
    file_path.open()
    parser = PDFParser(file_path)
    document = PDFDocument(parser, '')
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    a = ['result', ]
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for x in layout:
            if(isinstance(x, LTTextBox)):
                string = x.get_text()
                if(string != u'\n'):
                    a.append(string)
    file_path.close()
    return render(request, 'instruction.html', {'a':a, 'file_path':file_path })