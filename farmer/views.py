
import json

from django.shortcuts import render_to_response, redirect
from django.contrib.admin.views.decorators import staff_member_required

from farmer.models import Job

@staff_member_required
def home(request):
    if request.method == 'POST':
        inventories = request.POST.get('inventories', '')
        cmd = request.POST.get('cmd', '')
        if '' in [inventories.strip(), cmd.strip()]:
            return redirect('/')
        job = Job()
        job.inventories = inventories
        job.cmd = cmd
        job.run()
        return redirect('/')
    else:
        jobs = Job.objects.all().order_by('-id')
        return render_to_response('home.html', locals())

@staff_member_required
def detail(request, id):
    assert(request.method == 'GET')
    job = Job.objects.get(id = id)
    result = json.loads(job.result)
    failures = {}
    success = {}
    for k, v in result.items():
        if v.get('rc'):
            failures[k] = v
        else:
            success[k] = v
    return render_to_response('detail.html', locals())

@staff_member_required
def retry(request, id):
    assert(request.method == 'GET')
    job = Job.objects.get(id = id)
    result = json.loads(job.result)
    failures = {}
    for k, v in result.items():
        if v.get('rc'):
            failures[k] = v
    assert(failures)
    failures = failures.keys()
    newjob = Job()
    newjob.inventories = ':'.join(failures)
    newjob.cmd = job.cmd
    newjob.run()
    return redirect('/')


