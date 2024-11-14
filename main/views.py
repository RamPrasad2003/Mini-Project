from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from datetime import date
from Patient.models import *
from sklearn.svm import SVC
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from io import BytesIO

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
def gaurdainlogin(request):
    error=""
    if request.method=='POST':
        u=request.POST['emailid']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error='no'
            else:
                error='yes'
        except:
            error='yes'
    d={'error':error}
    return render(request,'gaurdianlogin.html',d)


def caresignup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        email=request.POST['emailid']
        pwd=request.POST['pwd']
        gender=request.POST['gender']
        dte=request.POST['dte']
        fie=request.FILES['pro']
        # print(fie)
        try:
            user=User.objects.create_user(username=email,password=pwd,first_name=f,last_name=l)
            CareTaker.objects.create(user=user,contact=con,gender=gender,dob=dte,facial_image=fie)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'caresignup.html',d)

def createpatient(request):
    if not request.user.is_authenticated:
        return redirect('gaurdainlogin')
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        email=request.POST['emailid']
        pwd=request.POST['pwd']
        gender=request.POST['gender']
        dte=request.POST['dte']
        fie=request.FILES['pro']
        care=request.user
        print(care)
        taker=CareTaker.objects.get(user=care)
        print(taker)
        try:
            user=User.objects.create_user(username=email,password=pwd,first_name=f,last_name=l)
            Patient.objects.create(user=user,contact=con,gender=gender,dob=dte,facial_image=fie,care=taker)
            error="no"
        except:
            error="yes"
    img=Patient.objects.all()
    d={'error':error,'abc':img}
    return render(request,'createpatient.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def viewpatient(request):
    if not request.user.is_authenticated:
        return redirect('gaurdainlogin')
    error=False
    user=User.objects.get(id=request.user.id)
    data=CareTaker.objects.get(user=user)
    users=Patient.objects.filter(care=data)
    d={'users':users}
    return render(request,'viewpatient.html',d)

def patientlogin(request):
    error=""
    if request.method=='POST':
        u=request.POST['emailid']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error='no'
            else:
                error='yes'
        except:
            error='yes'
    d={'error':error}
    return render(request,'patientlogin.html',d)

def patientedit(request,pid):
    if not request.user.is_authenticated:
        return redirect('gaurdainlogin')
    error=""
    # user=User.objects.get(id=pid)
    d=Patient.objects.get(id=pid)
    b={'d':d}
    return render(request,'Patientedit.html',b)


def changepass(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('gaurdianlogin')
    if request.POST:
        old=request.POST['old']
        new=request.POST['new']
        confirm=request.POST['confirm']
        if confirm==new:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(new)
            u.save()
            error='no'
        else:
            error='yes'
    d={'error':error}
    return render(request,'changepass.html',d)

def editprofile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error=False
    user=User.objects.get(id=request.user.id)
    data=CareTaker.objects.get(user=user)
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        c=request.POST['con']
        gender=request.POST['gender']
        dob=request.POST['dob']
        user.first_name=f
        user.last_name=l
        data.contact=c
        data.gender=gender
        data.dob=dob
        user.save()
        data.save()
        error=True
    d={'data':data,'user':user,'error':error}
    return render(request,'editprofile.html',d)

def gaurdianprofile(request):
    if not request.user.is_authenticated:
        return redirect('gaurdianlogin')
    error=False
    user=User.objects.get(id=request.user.id)
    data=CareTaker.objects.get(user=user)
    d={'d':data,'user':user}
    return render(request,'gaurdianprofile.html',d)

def addperson(request,pid):
    if not request.user.is_authenticated:
        return redirect('gaurdianlogin')
    error=""
    if request.method=='POST':
        patient=Patient.objects.get(id=pid)
        name=request.POST['name']
        dob=request.POST['dob']
        gender=request.POST['gender']
        relation=request.POST['relation']
        describe=request.POST['describe']
        file=request.FILES['pro']
        file_content = file.read()
        mtcnn = MTCNN()
        # print('nj:',file)
        resnet = InceptionResnetV1(pretrained='casia-webface').eval()
        img1 = Image.open(BytesIO(file_content))
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        faces1, _ = mtcnn.detect(img1)
        try:
            if faces1 is not None :
                aligned1 = mtcnn(img1)
                aligned1 = aligned1.unsqueeze(0) 
                embeddings1 = resnet(aligned1).detach()
                Person.objects.create(patient=patient,name=name,dob=dob,gender=gender,relation=relation,description=describe,facial_image=file,facial_embedding=embeddings1)
            error='no'
        except:
            error='yes'
    return render(request,'addperson.html')