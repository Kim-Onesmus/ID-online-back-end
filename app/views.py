from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Client, Notification, applyID, LocatioDetails, Photo, ConfirmationDocument, Photo, Contact, Pay, LostId, LostPay, BathNo, IDCard
from .forms import ClientForm, ConfirmationDocumentForm, PhotoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.conf import settings
import json
import requests
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image


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

def BirthNo(request):
    client = request.user.client
    birth = BathNo.objects.filter(client=client).first()
    apply_info = applyID.objects.filter(client=client).first()
    location_info = LocatioDetails.objects.filter(client=client).first()
    doc_info = ConfirmationDocument.objects.filter(client=client).first()
    photo_info = Photo.objects.filter(client=client).first()
    my_docs = ConfirmationDocument.objects.filter(client=client).first()

    if birth:
        return redirect('apply_id')
    if request.method == 'POST':
        birth_no = request.POST['birth_no']
        client=client

        if BathNo.objects.filter(birth_no=birth_no).exists():
            return redirect('birth_no')
        elif BathNo.objects.filter(client=client).exists():
            return redirect('birth_no')

        else:
            birht_details = BathNo.objects.create(client=client, birth_no=birth_no)
            birht_details.save()
            return redirect('apply_id')

    context = {'birth':birth, 'apply_info':apply_info, 'location_info':location_info, 'doc_info':doc_info, 'photo_info':photo_info, 'my_docs':my_docs}
    return render(request, 'app/birth_no.html', context)

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
    form = PhotoForm()
    if not photo_info:
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.client = request.user.client
                photo.status = 'pending'
                photo.save()
                return redirect('id_status')

        context = {'form':form}
        return render(request, 'app/take-photo.html', context)
    return redirect('applyIdDone')


@csrf_exempt
def savePhoto(request):
    if request.method == 'POST':
        try:
            form = PhotoForm(request.POST, request.FILES)

            if form.is_valid():
                print(form.cleaned_data)
                photo = form.save(commit=False)
                photo.client = request.user.client
                photo.status = 'pending'
                photo.save()
                
                return redirect('id_status')
                return JsonResponse({'status': 'success', 'photo_id': photo.id})
            else:
                print(form.errors)
                return JsonResponse({'status': 'error', 'message': 'Form is not valid'})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Failed to save photo'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def ApplyIdDone(request):
    client = request.user.client
    apply_info = applyID.objects.filter(client=client).first()
    location_info = LocatioDetails.objects.filter(client=client).first()
    doc_info = ConfirmationDocument.objects.filter(client=client).first()
    photo_info = Photo.objects.filter(client=client).first()
    my_docs = ConfirmationDocument.objects.filter(client=client).first()

    context = {'apply_info':apply_info, 'location_info':location_info, 'doc_info':doc_info, 'photo_info':photo_info, 'my_docs':my_docs}
    return render(request, 'app/ApplyIdDone.html', context)


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
    pay_details = Pay.objects.filter(client=client).first()
    lost_id = LostId.objects.filter(client=client).first()
    lost_pay = LostPay.objects.filter(client=client).first()
    if photo_info.status == 'approved' and my_docs and my_docs.status == 'approved':
        subject = 'ID application status updates'
        message = 'Your ID application status has beed updated. \n Please login to check the status of your application'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [client.email, ]
        send_mail( subject, message, email_from, recipient_list )

    context = {'my_docs':my_docs, 'photo_info':photo_info, 'pay_details':pay_details, 'lost_id':lost_id, 'lost_pay':lost_pay}
    return render(request, 'app/IdStatus.html', context)


def PayView(request):
    client = request.user.client
    pay_details = Pay.objects.filter(client=client).first()

    if pay_details:
        messages.info(request, 'You already payed for your id, if you you lost your ID you can apply for lost ID')
        return redirect('id_status')

    if request.method == 'POST':
        number = request.POST['number']
        amount = request.POST['amount']
        user = request.user

        if len(number) == 12 and (number.startswith('254') or number.startswith('2547')):
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}

            payload = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": number,
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": number,
                "CallBackURL": 'https://30de-105-160-60-50.ngrok-free.app/callback/',
                "AccountReference": "KimTech",
                "TransactionDesc": "Savings"
            }
            print('Payload', payload)

            response = requests.post(api_url, json=payload, headers=headers)
            print('response', response)

            if response.status_code == 200:
                mpesa_response = response.json()
                print('Mpesa Response', mpesa_response)
                
                # Check if 'ResponseCode' is in mpesa_response and its value is '0'
                if 'ResponseCode' in mpesa_response and mpesa_response['ResponseCode'] == '0':
                    deposit = Pay.objects.create(
                        client=client,
                        amount=amount,
                        number=number,
                    )
                    deposit.save()
                    
                    messages.success(request, 'Deposit successful')
                    return redirect('myID_url')
                else:
                    # Handle the case where the 'ResponseCode' is not '0'
                    messages.error(request, 'Deposit failed: ResponseCode is not 0')
            else:
                # Handle the case where the API call failed
                messages.error(request, 'M-Pesa API call failed')
        else:
            messages.error(request, f"Phone number '{number}' is not valid or in the wrong format")
            return redirect('pay_url')
    return render(request, 'app/pay.html')

def LostIDPay(request):
    client = request.user.client
    lostpayID = LostPay.objects.filter(client=client).first()
    print(lostpayID)

    if lostpayID:
        messages.info(request, 'You already paid for your lost ID')
        return redirect('id_status')

    if request.method == 'POST':
        number = request.POST['number']
        amount = request.POST['amount']
        user = request.user

        if len(number) == 12 and (number.startswith('254') or number.startswith('2547')):
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}

            payload = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": number,
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": number,
                "CallBackURL": 'https://30de-105-160-60-50.ngrok-free.app/callback/',
                "AccountReference": "KimTech",
                "TransactionDesc": "Savings"
            }
            print('Payload', payload)

            response = requests.post(api_url, json=payload, headers=headers)
            print('response', response)

            if response.status_code == 200:
                mpesa_response = response.json()
                print('Mpesa Response', mpesa_response)
                
                # Check if 'ResponseCode' is in mpesa_response and its value is '0'
                if 'ResponseCode' in mpesa_response and mpesa_response['ResponseCode'] == '0':
                    deposit = LostPay.objects.create(
                        client=client,
                        amount=amount,
                        number=number,
                    )
                    deposit.save()
                    
                    messages.success(request, 'Deposit successful')
                    return redirect('myID_url')
                else:
                    # Handle the case where the 'ResponseCode' is not '0'
                    messages.error(request, 'Deposit failed: ResponseCode is not 0')
            else:
                # Handle the case where the API call failed
                messages.error(request, 'M-Pesa API call failed')
        else:
            messages.error(request, f"Phone number '{number}' is not valid or in the wrong format")
            return redirect('lostpay_url')
    return render(request, 'app/lost_pay.html')

def LostID(request):
    client = request.user.client
    lost_id = LostId.objects.filter(client=client)

    if request.method == 'POST':
        client = client
        select = request.POST['select']
        text = request.POST['text']
        status = 'pending'

        lost_details = LostId.objects.create(client=client, select=select, text=text, status=status)
        lost_details.save()
        messages.info(request, 'Sumitted succesifully')
        return redirect('id_status')

    context = {'lost_id':lost_id}
    return render(request, 'app/lost_id.html', context)
 
def MyIDView(request):
    client = request.user.client
    id_details = IDCard.objects.filter(client=client).first()


    context = {'i':id_details}
    return render(request, 'app/my_id.html', context)

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

        subject = contact_details.subject
        message = f'Email from: {email} \n {contact_details.message}'
        email_from = contact_details.email
        recipient_list = [settings.EMAIL_HOST_USER, ]
        send_mail( subject, message, email_from, recipient_list )

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