from django.shortcuts import render
import random
# Create your views here.
def index(request):
    name='NEELDEEP',
    
    return render(request,'index.html',{'name':name})