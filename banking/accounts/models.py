from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BankBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Bank Balance for {self.user.username}"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=20)
    transfer_user = models.CharField(max_length=20, default="NULL")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tbalance =  models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction details for {self.user.username}"
