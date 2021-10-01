from django.urls import path, include
from . import views

urlpatterns = [
    
    path('login', views.loginUser),
    path('', views.index),
    path('internalTransfer', views.internalTransfer),
    path('logout', views.logoutUser),


]
