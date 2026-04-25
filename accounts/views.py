from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import User, Wallet, Transaction
from django.contrib.auth.decorators import login_required

def redirect_by_role(user):
    if user.is_staff or user.is_superuser:
        return redirect('/admin/')
    if user.is_driver():
        return redirect('/trips/dashboard/')
    # passenger ke liye
    return redirect('passenger_dashboard')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.get_or_create(user=user)

            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
            )

            if user is not None:
                login(request, user)
                return redirect_by_role(user)
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def old_driver_dashboard(request):
    return redirect('/trips/dashboard/')

def passenger_dashboard(request):
    return render(request, 'accounts/passenger_dashboard.html')

@login_required
def topup_wallet(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        if amount > 0:
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            wallet.balance += amount
            wallet.save()
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='topup'
            )
            messages.success(request, f'₹{amount} added to wallet!')
        return redirect('passenger_dashboard')
    return render(request, 'accounts/topup.html')

@login_required
def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        request.user.role = role
        request.user.save()

        return redirect_by_role(request.user)

    return render(request, 'accounts/choose_role.html')