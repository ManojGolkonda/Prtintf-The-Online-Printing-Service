from django.contrib import admin
from models import Customers,Merchants,Orders
# Register your models here.

admin.site.register([Customers, Merchants, Orders])

