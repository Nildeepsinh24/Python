from django.contrib import admin
from .models import Buyer, Seller, Cattle

admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Cattle)
