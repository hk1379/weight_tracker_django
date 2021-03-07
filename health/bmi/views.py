from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .models import Tracker
from django.contrib.auth.forms import UserCreationForm
#allows login, logout and authenticate methods to be used
from django.contrib.auth import authenticate, login, logout
#allows flash messages
from django.contrib import messages
#login_required methods allows you to restrict certain pages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    bmi = ""
    if request.method == 'POST':
        height = float(request.POST["height-field"])
        weight = int(request.POST["weight-field"])
        bmi = weight/ (height * height)
    return render(request, 'bmi/home.html', {'calculate_bmi':bmi})

def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account has been created for' + user)

                return redirect('login_page')


        context ={'form': form}
    return render(request, 'bmi/registration.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username-field')
            password = request.POST.get('password-field')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'bmi/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def weight_tracker(request):
    id = None
    name = ""
    date = ""
    weight = ""
    upload = ""
    if request.method == 'POST':
        id = None
        name = request.user
        date = request.POST["date-field"]
        weight = request.POST["weight-field"]
        upload = Tracker(id,name,date,weight)
        upload.save()
    return render(request, 'bmi/weight_tracker.html', {'weight': weight, 'date': date, 'upload': upload})

def weight_history(request, name):
    #weight_tracker_objs = Tracker.objects.get(pk=pk)
    #weight_tracker_objs1 = Tracker.objects.filter(id=pk)
    weight_tracker_objs1 = Tracker.objects.filter(name=name)
    context = {
        'tracker':weight_tracker,
    }
    return render(request, 'bmi/weight_history.html', {'context':context,'weight_tracker_objs1':weight_tracker_objs1})#, {'weight_tracker':weight_tracker})
