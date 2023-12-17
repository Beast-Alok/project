
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index"),
    path('deposit/', views.deposit, name="deposit"),
    path('withdrawl/', views.withdrawl, name="withdrawl"),
    path('transfer/', views.transfer, name="transfer"),
    path('transactions/', views.transactions, name="transactions"),

]
