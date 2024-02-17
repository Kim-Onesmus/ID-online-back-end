from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Client

# Create your views here.
def Register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if Client.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('/')
            else:
                user_details = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=password)
                user_details.save()
                
                client_details = Client.objects.create(first_name=first_name, last_name=last_name, email=email)
                client_details.save()

                messages.info(request, 'Account created')
                return redirect('login')
        else:
            messages.error(request, 'Password dont match')
            return redirect('/')
    return render(request, 'app/register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Welcome back')
            return redirect('index')
        else:
            messages.error(request, 'Invalid details')
            return redirect('login')
    return render(request, 'app/login.html')


def Index(request):
    return render(request, 'app/index.html')

def ApplyID(request):
    return render(request, 'app/applyID.html')


def MyDocuments(request):
    return render(request, 'app/myDocuments.html')

def IdStatus(request):
    return render(request, 'app/IdStatus.html')


def AboutUs(request):
    return render(request, 'app/aboutUs.html')


def ContactUs(request):
    return render(request, 'app/contact.html')


def AccountDetails(request):
    return render(request, 'app/accountDetails.html')

def UpdateAccount(request):
    return render(request, 'app/updateAccount.html')

def ChangePassword(request):
    return render(request, 'app/changePassword.html')

def LogOut(request):
    return render(request, 'app/logOut.html')