from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import BankBalance
# Create your views here.

def index(request):
    return render(request, 'index.html',)

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password') 

        if not email or not first_name or not last_name or not username or not password:
            messages.info(request,"Please fill in all the required fields.")
            return redirect('/register')
        
        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already exists. Please use a different email.")
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already exists. Please choose a different username.")
            return redirect('/register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password, first_name = first_name, last_name = last_name)
        new_user.save()

        # print(email,first_name,last_name,username,password)
        messages.info(request,"Registered Successfully !")
        return redirect('/login')
    return render(request, 'register.html')
    
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.info(request,"Please provide both username and password.")
            return redirect('/login')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/login_index')
        else:
            # print(username,password)
            messages.info(request,"Invalid username or password.")
            return redirect('/login')
        
    return render(request, 'login.html')

@login_required(login_url='/login')
def login_index(request):
    user_bank_balance, created = BankBalance.objects.get_or_create(user=request.user)
    balance = user_bank_balance.bank_balance
    # print(balance)
    # print(type(balance))
    return render(request, 'login_index.html',{'user':request.user,'balance':balance})

@login_required(login_url='/login')
def user_logout(request):
    auth_logout(request)
    return redirect('/login')