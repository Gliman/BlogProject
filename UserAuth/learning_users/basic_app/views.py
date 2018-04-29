from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")# set login url LOGIN_URL = '/basic_app/user_login/' settings.py!

@login_required
def user_logout(request):# Log out the user.
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()# save User Form to Database
            user.set_password(user.password)# hash the password
            user.save()# Update with Hashed password

            profile = profile_form.save(commit=False)
            profile.user = user# set One to One relationship between UserForm and UserProfileInfoForm
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']#grab it from the POST form reply

            profile.save()# save model
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)


        if user:
            if user.is_active:
                login(request,user)# log the user in.
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'basic_app/login.html', {})
