from django.shortcuts import render
from django.http import HttpResponse
from .models import Thread, Comment

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world")
    # return render(request, 'polls/index.html', context)
    return render(request, 'forum/index.html')
