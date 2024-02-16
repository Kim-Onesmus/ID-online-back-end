from django.shortcuts import render

# Create your views here.
def Register(request):
    return render(request, 'app/register.html')


def Login(request):
    return render(request, 'app/login.html')


def Index(request):
    return render(request, 'app/index.html')

def ApplyID(request):
    return render(request, 'app/applyID.html')


def MyDocuments(request):
    return render(request, 'app/myDocuments.html')

def IdStatus(request):
    return render(request, 'app/idStatus.html')


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