from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate
from django.shortcuts import redirect
# Create your views here.
def index(request):
    return render(request, 'index.html')

def lang(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    return render(request, 'lang.html',{'user':user})

def anothertrans(request):
    return render(request, 'anothertrans.html')

def options(request):
    if request.method == 'POST':
        options = request.POST.get('options')
        if options == 'withdrawal':
            return redirect('withdraw')
        elif options == 'transfer':
            return redirect('transfer')
        elif options == 'ballanceInquiry':
            return redirect('balenquiry')
        elif options == 'changepin':
            return redirect('changepin')
        else:
            print("else")
            return redirect('options')

    return render(request, 'options.html')

def password(request):
    if request.method == "POST":
        pin = request.POST.get('pin')
        account = Account.objects.get(pin=pin)
        if account:
            request.user = account.user
            request.session['username'] = request.user.username
            return redirect('lang')
        else:
            return render(request, 'password.html', {
                    "message": "Invalid credentials."
                })
    else:
        return render(request, 'password.html')
        
    

def successful(request):
    return render(request, 'successful.html')

def wait(request):
    return render(request, 'wait.html')

def withdraw(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
        amount = request.POST.get('amount')
        print(user)
        account = Account.objects.get(user=user)
        if account:
            account.balance -= int(amount)
            account.save()
            return redirect('successful')
        else:
            return render(request, 'withdraw.html', {
                    "message": "Invalid credentials."
                })
    return render(request, 'withdraw.html')

def transfer(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
        receiver_id = request.POST.get('receiver_id')
        amount = request.POST.get('amount')
        sender_account = Account.objects.get(user=user)
        receiver_account = Account.objects.get(account_id=receiver_id)
        if sender_account and receiver_account:
            sender_account.balance -= int(amount)
            sender_account.save()
            receiver_account.balance += int(amount)
            receiver_account.save()
            transfer = Transfer(sender=sender_account, receiver=receiver_account, amount=amount)
            transfer.save()
            return redirect('successful')
        else:
            print("ok")
            return render(request, 'transfer.html', {
                    "message": "Invalid credentials."
                })
    else:
        print("lol else")
        return render(request, 'transfer.html')

def balenquiry(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)
    if account:
        return render(request, 'balenquiry.html', {
            "account": account
        })
    return render(request, 'balenquiry.html')

def changepin(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
        oldpin = request.POST.get('oldpin')
        newpin = request.POST.get('newpin')
        account = Account.objects.get(user=user)
        if account:
            if account.pin == oldpin:
                account.pin = newpin
                account.save()
                return redirect('successful')
            else:
                return render(request, 'changepin.html', {
                    "message": "Invalid credentials."
                })
    return render(request, 'changepin.html')