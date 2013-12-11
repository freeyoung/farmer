
from django.shortcuts import render_to_response, redirect

from farmer.models import Job

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
        jobs = Job.objects.all()
        return render_to_response('home.html', locals())
