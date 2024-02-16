from django.urls import path
from . import views

urlpatterns = [
    path('', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('index', views.Index, name='index'),
    path('apply_id', views.ApplyID, name='apply_id'),
    path('my_documents', views.MyDocuments, name='my_documents'),
    path('id_status', views.IdStatus, name='id_status'),
    path('about_us', views.AboutUs, name='about_us'),
    path('contact_us', views.ContactUs, name='contact_us'),
    path('account_details', views.AccountDetails, name='account_details'),
    path('update_account', views.UpdateAccount, name='update_account'),
    path('change_password', views.ChangePassword, name='change_password'),
    path('logout', views.LogOut, name='logout'),
]