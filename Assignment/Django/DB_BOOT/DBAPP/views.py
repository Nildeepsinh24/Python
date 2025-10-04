from django.shortcuts import render,redirect

from DBAPP.forms import StudInfoForm
from DBAPP.models import Studinfo
from .forms import *

# Create your views here.
def index(request):
    if request.method=='POST': #TRUE
        form=StudInfoForm(request.POST)
        if form.is_valid():
            form.save()
            print("Record Inserted!")
        else:
            print(form.errors)
    return render(request,'index.html')

def showdata(request):
    stdata=Studinfo.objects.all()
    print(stdata)
    return render(request,'showdata.html',{'stdata':stdata})

def updatedata(request,id):
    stid=Studinfo.objects.get(id=id)
    if request.method=='POST': #TRUE
        form=StudInfoForm(request.POST,instance=stid)
        if form.is_valid():
            form.save()
            print("Record Updated!")
            return redirect('showdata')
        else:
            print(form.errors)
    return render(request,'updatedata.html',{'stid':stid})

def deletedata(request,id):
    stid=Studinfo.objects.get(id=id)
    Studinfo.delete(stid)
    return redirect('showdata')

