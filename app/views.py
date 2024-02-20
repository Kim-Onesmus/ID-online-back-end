from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Client, Notification, applyID, LocatioDetails, Photo, ConfirmationDocument, Photo, Contact
from .forms import ClientForm, ConfirmationDocumentForm, PhotoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

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
    client = request.user.client
    apply_info = applyID.objects.filter(client=client)
    notes = Notification.objects.all()

    context = {'notes':notes, 'apply_info':apply_info}
    return render(request, 'app/index.html', context)

def Apply_ID(request):
    client = request.user.client
    apply_info = applyID.objects.filter(client=client).first()
    location_info = LocatioDetails.objects.filter(client=client).first()
    doc_info = ConfirmationDocument.objects.filter(client=client).first()
    photo_info = Photo.objects.filter(client=client).first()
    my_docs = ConfirmationDocument.objects.filter(client=client).first()

    if apply_info:
        return redirect('location')
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
        elif middle_name == 'None':
            messages.error(request, 'Update your account to continue')
            return redirect('update_account')
        else:
            apply_details = applyID.objects.create(client=client, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth)
            apply_details.save()
            return redirect('location')

    context = {'apply_info':apply_info, 'location_info':location_info, 'doc_info':doc_info, 'photo_info':photo_info, 'my_docs':my_docs}
    return render(request, 'app/applyID.html', context)

def LocationData(request):
    client = request.user.client
    location_info = LocatioDetails.objects.filter(client=client).first()
    if not location_info:
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
    return redirect('confirmation_documents')

def ConfirmationDocuments(request):
    client = request.user.client
    doc_info = ConfirmationDocument.objects.filter(client=client).first()
    if not doc_info:
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
    return redirect('take_photo')

def TakePhoto(request):
    client = request.user.client
    photo_info = Photo.objects.filter(client=client).first()
    if not photo_info:
        return render(request, 'app/take-photo.html')
    return redirect('applyIdDone')

def ApplyIdDone(request):
    client = request.user.client
    apply_info = applyID.objects.filter(client=client).first()
    location_info = LocatioDetails.objects.filter(client=client).first()
    doc_info = ConfirmationDocument.objects.filter(client=client).first()
    photo_info = Photo.objects.filter(client=client).first()
    my_docs = ConfirmationDocument.objects.filter(client=client).first()

    context = {'apply_info':apply_info, 'location_info':location_info, 'doc_info':doc_info, 'photo_info':photo_info, 'my_docs':my_docs}
    return render(request, 'app/ApplyIdDone.html', context)

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import base64

@csrf_exempt
def savePhoto(request):
    if request.method == 'POST':
        try:
            image_data = request.FILES.get('image')

            # You can use SimpleUploadedFile to create a Django UploadedFile instance
            uploaded_file = SimpleUploadedFile('image.jpg', image_data.read())

            form = PhotoForm({'image': uploaded_file})

            if form.is_valid():
                photo = form.save(commit=False)
                photo.client = request.user.client  # Assuming you have authentication in place
                photo.status = 'pending'
                photo.save()

                return JsonResponse({'status': 'success', 'photo_id': photo.id})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Failed to save photo'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def MyDocuments(request):
    client = request.user.client
    my_docs = ConfirmationDocument.objects.filter(client=client)
    photo_info = Photo.objects.filter(client=client).first()

    context = {'my_docs':my_docs, 'photo_info':photo_info}
    return render(request, 'app/myDocuments.html', context)

def IdStatus(request):
    client = request.user.client
    my_docs = ConfirmationDocument.objects.filter(client=client)
    photo_info = Photo.objects.filter(client=client).first()

    context = {'my_docs':my_docs, 'photo_info':photo_info}
    return render(request, 'app/IdStatus.html', context)


def AboutUs(request):
    return render(request, 'app/aboutUs.html')


def ContactUs(request):
    if request.method == 'POST':
        client = request.user.client
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact_details = Contact.objects.create(client=client, name=name, email=email, subject=subject, message=message)
        contact_details.save()
        message.info(request, 'Messange sent')
        return redirect('index')

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