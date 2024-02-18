from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Client, Notification, applyID, LocatioDetails, Photo
from .forms import ClientForm, ConfirmationDocumentForm, PhotoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
import cv2
import numpy as np

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
    notes = Notification.objects.all()

    context = {'notes':notes}
    return render(request, 'app/index.html', context)

def ApplyID(request):
    if request.method == 'POST':
        client = request.user.client
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']

        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if applyID.objects.filter(client=client).exists():
            messages.error(request, 'You already applied for ID, check your ID status')
            return redirect('apply_id')
        elif age < 18:
            messages.info(request, 'You cannot apply ID, you are under age')
            return redirect('apply_id')
        else:
            apply_details = applyID.objects.create(client=client, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth)
            apply_details.save()
            return redirect('location')
    else:
        return render(request, 'app/applyID.html')
    return render(request, 'app/applyID.html')

def LocationData(request):
    if request.method == 'POST':
        client = request.user.client
        county = request.POST['county']
        sub_county = request.POST['sub_county']
        district = request.POST['district']
        division = request.POST['division']
        location = request.POST['location']
        sub_location = request.POST['sub_location']
        village = request.POST['village']
        land_mark = request.POST['land_mark']

        lacatio_data = LocatioDetails.objects.create(client=client, date=date, county=county, sub_county=sub_county, district=district, division=division, location=location, sub_location=sub_location, village=village, land_mark=land_mark)
        lacatio_data.save()
        return redirect('confirmation_documents')
    else:
        return render(request, 'app/location.html')
    return render(request, 'app/location.html')

def ConfirmationDocuments(request):
    form = ConfirmationDocumentForm()
    if request.method == 'POST':
        form = ConfirmationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            confirmation_document = form.save(commit=False)
            confirmation_document.client = request.user.client
            confirmation_document.status = 'pending'
            confirmation_document.save()
            return redirect('take_photo')

        else:
            print(form.errors)

    context = {'form':form}
    return render(request, 'app/confirmationDocs.html', context)

def TakePhoto(request):
    return render(request, 'app/take-photo.html')


@csrf_exempt
def savePhoto(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data', '')
        image_data = image_data.split(',')[1]  # Remove "data:image/jpeg;base64,"

        decoded_image = base64.b64decode(image_data)

        image = Image.open(BytesIO(decoded_image))

        form = PhotoForm({'image': image})

        if form.is_valid():
            photo = form.save(commit=False)
            photo.client = request.user.client
            photo.status = 'pending'  # Set a default status if needed
            photo.save()

            return JsonResponse({'status': 'success', 'photo_id': photo.id})

    return JsonResponse({'status': 'error'})

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
    if request.method == 'POST':
        auth.logout(request)
        messages.info(request, 'Logged Out')
        return redirect('login')
    return render(request, 'app/logOut.html')