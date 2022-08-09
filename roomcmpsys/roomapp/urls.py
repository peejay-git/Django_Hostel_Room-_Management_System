from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # shared urls
    path('', views.login_form, name="home"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    
    # Hall Supervisor urls
    path('supervisor/', views.supervisor, name="supervisor"),
    path('asearch/', views.asearch, name="asearch"),
    path('smcomplain/', views.SManageComplain.as_view(), name="smcomplain"),
    path('secomplain/<int:pk>', views.SEditComplaintView.as_view(), name="secomplain"),
    path('svcomplain/<int:pk>', views.SViewComplain.as_view(), name="svcomplain"),
  
    
    
    # student urls
    path('student/', views.ComplaintListView.as_view(), name="student"),
    path('my_complaint/<str:username>', views.MyComplaintListView.as_view(), name="my_complaint"),
    path('complaintForm/', views.ComplaintView.as_view(), name="complaintForm"),
    
]

