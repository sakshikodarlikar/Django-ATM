from .models import *
from django.contrib.auth import authenticate
from .form import ImageForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
from django.views.decorators import gzip
import threading
import validators
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math
import random
# Create your views here.


def index(request):
    return render(request, 'index.html')


def lang(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    return render(request, 'lang.html', {'user': user})


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
        # qrcode = request.session['qrcode']
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
            transfer = Transfer(sender=sender_account,
                                receiver=receiver_account, amount=amount)
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


def redirect_view(request):
    # print("hellos")
    return HttpResponseRedirect('https://simpleblog.com/posts/archive/')
    response = redirect('/test/')

    return redirect('http://google.com')


barcode = ""
isURL = True


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image = read_barcodes(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    def stop(self):
        self.video.release()

    def __del__(self):
        self.video.release()


def read_barcodes(frame):
    global barcode, isURL
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect  # 1
        barcode_info = barcode.data.decode('utf-8')
        barcode = barcode_info
        isURL = validators.url(barcode)
        # print(barcode)
        camOn = False
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6),
                    font, 2.0, (255, 255, 255), 1)  # 3
        with open("barcode_result.txt", mode='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
            print(barcode_info)
            # request.session['qrcode'] = barcode_info
    return frame


def gen(camera, request):
    global barcode, isURL
    while True:
        frame = camera.get_frame()
        if len(barcode) > 0:
            camera.stop()
            break
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    redirect_view(request)


@gzip.gzip_page
def livefe(request):
    global barcode, isURL
    if len(barcode) > 0:
        barcode = ""
        # print("in live fun if")
    try:
        cam = VideoCamera()
        # print("test")
        print(barcode)
        return StreamingHttpResponse(gen(cam, request), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("test")  # This is bad! replace it with proper handling
        pass

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.


def ScannerView(request):
    global barcode, isURL
    return render(request, 'sc.html', {"barcode":  barcode, "isUrl": isURL})


def getBarcode(request):
    global barcode, isURL
    print("in fun")
    print(barcode)
    return render(request, 'barcode.html', {"barcode":  barcode, "isUrl": isURL})


def Get_image_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            q2 = Image.objects.latest('id')
            print(type(q2))
            img = cv2.imread('q2.Main_Img.url')
            print(type(img))
            print(decode(img))
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'barcode.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


def otp(request):
    return render(request, "otp.html")


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(request):
    email = request.GET.get("email")
    print(email)
    o = generateOTP()
    htmlgen = '<p>Your OTP is <strong>o</strong></p>'
    # send_mail('OTP request', o, '<your gmail id>', [email], fail_silently=False, html_message=htmlgen)
    print(o)
    return HttpResponse(o)
