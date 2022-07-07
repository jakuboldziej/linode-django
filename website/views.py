from django.shortcuts import render, redirect
from .models import Image
import os

from smsapi.client import SmsApiPlClient

smsapi_access_token = 'L3LlVvkfevSgw0wqeADhLEYLkc6Z27FCzrGm9aeH'

# Pages
def index(request):
    return render(request, 'index.html')

# 404 Handling
def view_page_not_found(request, exception):
    return render(request, '404.html')

def slider(request):
    image_object = Image.objects.all()
    context = {
        'images': image_object, 
    }
    return render(request, 'slider.html', context)

def smsapi(request):
    return render(request, 'smsapi.html')

def polls(request):
    return render(request, 'polls.html')

# Events

def sendsms(request):
    if request.method == 'POST':
        client = SmsApiPlClient(access_token=smsapi_access_token)
        smsreceiver = "+48" + request.POST['smsreceiver']
        smsmessage = request.POST['smsmessage']
        print(smsreceiver, smsmessage)
        client.sms.send(to=smsreceiver, message=smsmessage)

        return redirect('/smsapi/')