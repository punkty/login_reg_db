from django.shortcuts import render, redirect
from .models import User
import re
import bcrypt
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import hashlib


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")

def process(request):
    errors = []
    user = User.objects.filter(email=request.POST['email'])


    if not request.POST['email']:
        errors.append("Email cannot be blank.")
    elif not EMAIL_REGEX.match(request.POST['email']):
        errors.append("Must be a valid email.")
    elif user:
        errors.append('Email is already in use.')

    if not request.POST['first_name']:
        errors.append("First name cannot not not be blank.")
    elif not request.POST['last_name']:
        errors.append("Last name cannot not not be blank.")

    if not request.POST['password']:
        errors.append("Password cannot not not be blank.")
    elif len(request.POST['password']) < 8:
        errors.append("Password must be at least 8 characters.")
    elif request.POST['password'] != request.POST['confirm']:
        errors.append('Password and confirm password must match.')

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        User.objects.create(email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        user_id = User.objects.filter(email=request.POST['email'])[0].id
        request.session['user_id'] = user_id

        return redirect('/success')

def login(request):
    errors = []
    user = User.objects.all().filter(email=request.POST['email'])

    if not user:
        errors.append("Invalid login.")

    if errors:
        for error in errors:
            messages.error(request, error)
            return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        request.session["user_id"] = User.objects.get(email=request.POST['email']).id
        return redirect("/success")
    else:
        errors.append("Invalid login.")

    if errors:
        for error in errors:
            messages.error(request, error)
            return redirect('/')

def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    name = User.objects.all().filter(id = request.session['user_id'])
    context = {

        'first_name': name[0].first_name
    }
    return render(request, "login_registration/success.html", context)

def clear(request):
    request.session.clear()
    return redirect('/')
