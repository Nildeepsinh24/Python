from django.shortcuts import render
from .forms import *
# Create your views here.
def index(request):
    if request.method=='POST':
        st=studinfoForms(request.POST)
        if st.is_valid():
            st.save()
            print("Record Inserted")
        else:
            print(st.errors)
    return render(request,'index.html')