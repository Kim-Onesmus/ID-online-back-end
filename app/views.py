from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Client
from .forms import ClientForm

# Create your views here.
def Register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if Client.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('/')
            elif Client.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('/')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()
                
                client_details = Client.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, username=username, gender=gender)
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
    user = request.user
    client = Client.objects.filter(user=user)

    context = {'client':client}
    return render(request, 'app/accountDetails.html', context)

def UpdateAccount(request):
    try:
        user = request.user
        client = Client.objects.filter(user=user).first()
        form = ClientForm(instance=client)
        if request.method == 'POST':
            form = ClientForm(request.POST, request.FILES, instance=client)
            if form.is_valid():
                form.save()
                messages.info(request, 'Account updated')
                return redirect('update_account')

        context = {'client':client, 'form':form}
        return render(request, 'app/updateAccount.html', context)

    except Exception as e:
        # Handle other exceptions if needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('attendance')

def ChangePassword(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.info(request, 'Password updated')
            return redirect('login')
    
    context = {'password_form':password_form}
    return render(request, 'app/changePassword.html', context)

def LogOut(request):
    return render(request, 'app/logOut.html')