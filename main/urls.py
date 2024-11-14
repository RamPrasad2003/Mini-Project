from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("gaurdainlogin",gaurdainlogin,name='gaurdainlogin'),
    path("caresignup",caresignup,name='caresignup'),
    path("createpatient",createpatient,name='createpatient'),
    path("Logout",Logout,name='Logout'),
    path("viewpatient",viewpatient,name='viewpatient'),
    path("patientlogin",patientlogin,name='patientlogin'),
    path("about",about,name='about'),
    path("patientedit/<int:pid>",patientedit,name='patientedit'),
    path("changepass",changepass,name='changepass'),
    path("editprofile",editprofile,name='editprofile'),
    path("gaurdianprofile",gaurdianprofile,name='gaurdianprofile'),
    path("addperson/<int:pid>",addperson,name='addperson'),
]