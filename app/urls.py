from django.urls import path
from . import views
from .views import savePhoto

urlpatterns = [
    path('', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('index', views.Index, name='index'),
    path('apply_id', views.Apply_ID, name='apply_id'),
    path('applyIdDone', views.ApplyIdDone, name='applyIdDone'),
    path('location', views.LocationData, name='location'),
    path('confirmation_documents', views.ConfirmationDocuments, name='confirmation_documents'),
    path('take_photo', views.TakePhoto, name='take_photo'),
    path('save_photo/', savePhoto, name='save_photo'),
    path('my_documents', views.MyDocuments, name='my_documents'),
    path('id_status', views.IdStatus, name='id_status'),
    path('los_id', views.LostID, name='lost_id'),
    path('pay_id', views.PayView, name='pay_url'),
    path('my_id', views.MyIDView, name='myID_url'),

    path('about_us', views.AboutUs, name='about_us'),
    path('contact_us', views.ContactUs, name='contact_us'),
    path('account_details', views.AccountDetails, name='account_details'),
    path('update_account', views.UpdateAccount, name='update_account'),
    path('change_password', views.ChangePassword, name='change_password'),
    path('logout', views.LogOut, name='logout'),
]