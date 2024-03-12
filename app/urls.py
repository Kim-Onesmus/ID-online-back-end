from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import savePhoto

urlpatterns = [
    path('', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('index', views.Index, name='index'),
    path('birth_no', views.BirthNo, name='birth_no'),
    path('apply_id', views.Apply_ID, name='apply_id'),
    path('applyIdDone', views.ApplyIdDone, name='applyIdDone'),
    path('location', views.LocationData, name='location'),
    path('confirmation_documents', views.ConfirmationDocuments, name='confirmation_documents'),
    path('take_photo', views.TakePhoto, name='take_photo'),
    path('save_photo/', savePhoto, name='save_photo'),
    path('my_documents', views.MyDocuments, name='my_documents'),
    path('id_status', views.IdStatus, name='id_status'),
    path('lost_id', views.LostID, name='lost_id'),
    path('pay_id', views.PayView, name='pay_url'),
    path('lostpay_id', views.LostIDPay, name='lostpay_url'),
    path('my_id', views.MyIDView, name='myID_url'),

    path('about_us', views.AboutUs, name='about_us'),
    path('contact_us', views.ContactUs, name='contact_us'),
    path('account_details', views.AccountDetails, name='account_details'),
    path('update_account', views.UpdateAccount, name='update_account'),
    path('change_password', views.ChangePassword, name='change_password'),
    path('logout', views.LogOut, name='logout'),
    
    
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="app/passwordReset/forget-password.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="app/passwordReset/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="app/passwordReset/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="app/passwordReset/password_reset_done.html"), 
        name="password_reset_complete"),
]