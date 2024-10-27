from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import datetime
import random
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout

def log_in(request):
    error = ''

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            # get user model
            user = User.objects.get(email=form.cleaned_data['email'])

            auth_user = authenticate(
                request, 
                username=user.username, 
                password=form.cleaned_data['password']
            )

            if auth_user is None:
                return render(request, "user/login.html", {
                    'title': 'Login',
                    'error': 'Invalid username or password !',
                })

            login(request, auth_user)

            messages.success(request, "Welcome back !")
            return redirect('/')
        else:
            for error in form.errors.keys():
                if error == 'email':
                    error = 'Invalid username or password !'
                    break
                elif error == 'password':
                    error = 'Invalid username or password !'
                    break

    return render(request, "user/login.html", {
        'title': 'Login',
        'error': error,
    }) 

def register(request):
    error = ''

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            #check email
            email_exists = User.objects.filter(email=form.cleaned_data['email'])

            if len(email_exists) > 0:
                return render(request, "user/register.html", {
                    'title': 'Register',
                    'error': 'This email address already exists !',
                }) 
            
            #check password
            if form.cleaned_data['password'] != form.cleaned_data['confirm']:
                return render(request, "user/register.html", {
                    'title': 'Register',
                    'error': 'Password and the confirmation are not matched !',
                })

            # create username and password
            username = (form.cleaned_data['first_name'] + 
                form.cleaned_data['last_name'] + 
                str(random.randint(0, 99999999999))
            )

            password = make_password(form.cleaned_data['password'])
            
            # create new user model
            user = User.objects.create(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = password,
                date_joined = datetime.datetime.now(),
                is_active = True,
                is_staff = False,
                is_superuser = False,
                username = username,
            )

            login(request, user)

            messages.success(request, "Congratulations , Your account has been created successfully !")
            return redirect('/')
        else:
            for error in form.errors.keys():
                if error == 'first_name':
                    error = 'Invalid first name !'
                    break
                elif error == 'last_name':
                    error = 'Invalid last name !'
                    break
                elif error == 'email':
                    error = 'Invalid email !'
                    break
                elif error == 'password':
                    error = 'Invalid password !'
                    break
                elif error == 'confirm':
                    error = 'Invalid confirm password !'
                    break

    return render(request, "user/register.html", {
        'title': 'Register',
        'error': error,
    }) 

def log_out(request):
    logout(request)
    messages.success(request, "Bye !!")
    return redirect('/')

def profile(request):
    pass