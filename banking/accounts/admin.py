from django.contrib import admin
from .models import BankBalance,Transaction
# Register your models here.

admin.site.register(BankBalance)
admin.site.register(Transaction)