from django.shortcuts import render, redirect
from .models import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login_registration/index.html')

def process(request):

    return redirect('/')

    return render(request, 'login_registration/success.html')
