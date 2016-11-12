from django.shortcuts import render, redirect
from .models import User
import re
import bcrypt
from django.contrib import messages


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")

def process(request):
    print request.POST
    error = []
    if not request.POST['email']:
        error.append("Email cannot be blank")
        return redirect("/")
    elif not EMAIL_REGEX.match(request.POST['email']):
        error.append( "Must be a valid email")
        return redirect("/")
    elif not request.POST['first_name']:
        messages.error(request, "Name must not be blank")
    elif not request.POST['last_name']:
        messages.error(request, "Name must not be blank")


    User.objects.create(email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))

    cats = User.objects.filter(email=request.POST['email'])
    print cats.query
    print '**********************************************************'
    email = request.POST['email']
    print(email)
    print '**********************************************************'


    request.session['email'] = email
    Email.objects.create(email=email)

    return redirect('/success')

def success(request):
    if "email" not in request.session:
        return redirect("/")
    context = {
        'emails': Email.objects.all(),
    }
    return render(request, "login_registration/success.html", context)

def clear(request):
    request.session.clear()
    return redirect('/')
