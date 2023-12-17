from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BankBalance,Transaction
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/login')
def index(request):
    pass

@login_required(login_url='/login')
def deposit(request):
    if request.method == 'POST':
        user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
        amount = request.POST.get('amount')
        if not amount:
            messages.info(request,"Please enter amount before proceed !")
            return redirect('/accounts/deposit')
        else:
            new_amount = Decimal(amount)
            user_bank_balance.bank_balance += new_amount
            user_bank_balance.save()
            #to record transcations details
            transfer_transaction_receiver = Transaction.objects.create(
                user=request.user,
                mode='Deposit',
                amount=new_amount,
                tbalance = user_bank_balance.bank_balance,
                timestamp=datetime.now()
            )
            transfer_transaction_receiver.save()

            messages.info(request,"Money deposited successfully !")
            return redirect('/accounts/deposit')
    user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
    balance = user_bank_balance.bank_balance
    return render(request, 'deposit.html', {'user':request.user,'balance':balance})

@login_required(login_url='/login')
def withdrawl(request):
    if request.method == 'POST':
        user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
        amount = request.POST.get('amount')
        if not amount:
            messages.info(request,"Please enter amount before proceed !")
            return redirect('/accounts/withdrawl')
        else:
            new_amount = Decimal(amount)
            if (user_bank_balance.bank_balance <= 0 or new_amount > user_bank_balance.bank_balance):
                messages.info(request,"You have insufficient balance !")
                return redirect('/accounts/withdrawl')   
            else:
                user_bank_balance.bank_balance -= new_amount
                user_bank_balance.save()

                #to record transcations details
                transfer_transaction_receiver = Transaction.objects.create(
                    user=request.user,
                    mode='Withdrawl',
                    amount=new_amount,
                    tbalance = user_bank_balance.bank_balance,
                    timestamp=datetime.now()
                )
                transfer_transaction_receiver.save()

                messages.info(request,"Money withdrawled successfully !")
                return redirect('/accounts/withdrawl')
    user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
    balance = user_bank_balance.bank_balance
    return render(request, 'withdrawl.html', {'user':request.user,'balance':balance})


def get_bank_balance_by_username(username):
    try:
        user = User.objects.get(username=username)
        bank_balance, _ = BankBalance.objects.get_or_create(user=user)
        return bank_balance
    except User.DoesNotExist:
        return None

@login_required(login_url='/login')
def transfer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        amount = request.POST.get('amount')
        if not amount:
            messages.info(request,"Please enter all the required field !")
            return redirect('/accounts/transfer')
        else:
            receiver_username = get_bank_balance_by_username(username)

            if receiver_username is None:
                messages.info(request,"Invalid username !")
                return redirect('/accounts/transfer')
            
            new_amount = Decimal(amount)
            user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
            if (user_bank_balance.bank_balance <= 0 or new_amount > user_bank_balance.bank_balance):
                messages.info(request,"You have insufficient balance !")
                return redirect('/accounts/transfer')
            else:
                receiver_username.bank_balance += new_amount
                user_bank_balance.bank_balance -= new_amount
                user_bank_balance.save()
                receiver_username.save()

                if receiver_username.user.username == user_bank_balance.user.username:
                    messages.info(request,"You cannot transfer money to yourself !")
                    return redirect('/accounts/transfer')
                else:
                    #to record transcations details
                    transfer_transaction_receiver = Transaction.objects.create(
                        user=request.user,
                        mode='Transfer',
                        transfer_user = receiver_username.user.username,
                        amount=new_amount,
                        tbalance = user_bank_balance.bank_balance,
                        timestamp=datetime.now()
                    )
                    transfer_transaction_receiver.save()

                    #to record transaction details at recevier side also
                    transfer_transaction_receiver = Transaction.objects.create(
                        user=receiver_username.user,
                        mode='Received',
                        transfer_user = user_bank_balance.user.username,
                        amount=new_amount,
                        tbalance = receiver_username.bank_balance,
                        timestamp=datetime.now()
                    )
                    transfer_transaction_receiver.save()
                    messages.info(request,"Money transfered successfully !")
                    return redirect('/accounts/transfer')
    user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
    balance = user_bank_balance.bank_balance
    return render(request, 'transfer.html', {'user':request.user,'balance':balance})

            
@login_required(login_url='/login')
def transactions(request):
    user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
    balance = user_bank_balance.bank_balance
    # user_transactions = Transaction.objects.filter(user=request.user)
    # user_transactions = Transaction.objects.order_by('-timestamp')
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    # print(user_transactions)
    return render(request, 'transactions.html', {'transactions': user_transactions, 'balance':balance})
