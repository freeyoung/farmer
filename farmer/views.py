
from django.shortcuts import render_to_response, redirect

from farmer.models import Job

def home(request):
    if request.method == 'POST':
        inventories = request.POST.get('inventories', None)
        cmd = request.POST.get('cmd', None)
        job = Job()
        job.inventories = inventories
        job.cmd = cmd
        job.run()
        return redirect('/')
    else:
        return render_to_response('home.html', locals())
