from django.shortcuts import render_to_response

def home(request):
    readme = open('README.md').read()
    return render_to_response('index.html', locals())
