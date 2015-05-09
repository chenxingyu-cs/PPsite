from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from disk.models import Project, Version

# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated():
        u = request.user
        latest_project_list = Project.objects.filter(user_id=u.id).order_by('-pub_date')
        context =  {'latest_project_list': latest_project_list, 'u':u}
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/signin/')