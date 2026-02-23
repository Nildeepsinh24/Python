from django.shortcuts import render, redirect
from .models import Buyer, Seller, Cattle

def home(request):
    return render(request, 'home.html')

def register_buyer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        Buyer.objects.create(name=name, contact=contact, address=address)
        return redirect('home')
    return render(request, 'register_buyer.html')

def register_seller(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        Seller.objects.create(name=name, contact=contact, address=address)
        return redirect('home')
    return render(request, 'register_seller.html')

def add_cattle(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        price = request.POST.get('price')
        Cattle.objects.create(name=name, breed=breed, age=age, price=price)
        return redirect('cattle_list')
    return render(request, 'add_cattle.html')

def cattle_list(request):
    cattles = Cattle.objects.all()
    return render(request, 'cattle_list.html', {'cattles': cattles})
