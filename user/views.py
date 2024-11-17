from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import datetime
import random
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .decorators import user_is_guest, user_is_auth
from shop.models import Address

@user_is_guest
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

@user_is_guest
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

@user_is_auth
def log_out(request):
    logout(request)
    messages.success(request, "Bye !!")
    return redirect('/')

@user_is_auth
def profile(request):
    error = ''

    if request.method == "POST":
        form = ProfileForm(request.POST)
        user = request.user

        if form.is_valid():
            # check old password and new password , and update the password
            # if form.cleaned_data['password'] != form.cleaned_data['confirm']:
            #     return render(request, "user/profile.html", {
            #         'title': 'Register',
            #         'error': 'Password and the confirmation are not matched !',
            #     })

            # password = make_password(form.cleaned_data['password'])
            
            # update user model
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']

            if user.address:
                user.address.phone = form.cleaned_data['phone']
                user.address.country = form.cleaned_data['country']
                user.address.state = form.cleaned_data['state']
                user.address.city = form.cleaned_data['city']
                user.address.details = form.cleaned_data['details']
                user.address.postcode = form.cleaned_data['postcode']
                
                user.address.save()
            else:
                address = Address.objects.create(
                    user_id = user.id,
                    phone = form.cleaned_data['phone'],
                    country = form.cleaned_data['country'],
                    state = form.cleaned_data['state'],
                    city = form.cleaned_data['city'],
                    details = form.cleaned_data['details'],
                    postcode = form.cleaned_data['postcode']    
                )

            user.save()

            messages.success(request, "Congratulations , Your account has been updated successfully !")
            return redirect('/')
        else:
            for error in form.errors.keys():
                if error == 'first_name':
                    error = 'Invalid first name !'
                    break
                elif error == 'last_name':
                    error = 'Invalid last name !'
                    break
                elif error == 'phone':
                    error = 'Invalid phone !'
                    break
                elif error == 'country':
                    error = 'Invalid country !'
                    break
                elif error == 'state':
                    error = 'Invalid state !'
                    break
                elif error == 'city':
                    error = 'Invalid city !'
                    break
                elif error == 'details':
                    error = 'Invalid address !'
                    break
                # elif error == 'password':
                #     error = 'Invalid password !'
                #     break
                # elif error == 'confirm':
                #     error = 'Invalid confirm password !'
                #     break

    return render(request, "user/profile.html", {
        'title': 'Profile',
        'error': error,
    }) 