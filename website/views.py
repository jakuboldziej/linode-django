from django.shortcuts import render, redirect
from .models import Image, TwoOptionPoll
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
    poll_object = TwoOptionPoll.objects.all()
    context ={
        'polls': poll_object,
    }
    return render(request, 'polls.html', context)

def createpoll(request):
    if request.method == 'POST':
        question = request.POST['question']
        option_one = request.POST['optionone']
        option_two = request.POST['optiontwo']
        print(question, option_one, option_two)

        new_poll = TwoOptionPoll.objects.create(question=question, option_one=option_one, option_two=option_two)
        new_poll.save()
        return redirect('polls')
    else:
        return render(request, 'createpoll.html')

def poll(request, poll_id):
    poll = TwoOptionPoll.objects.get(id=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1

        poll.save()
        return redirect('polls')
    else:
        poll_object = TwoOptionPoll.objects.get(id=poll_id)
        context = {'poll': poll_object}

        return render(request, 'vote.html', context)

def results(request, poll_id):
    poll = TwoOptionPoll.objects.get(id=poll_id)

    context ={
        'poll': poll
    }
    return render(request, 'results.html', context)
# Events

def sendsms(request):
    if request.method == 'POST':
        client = SmsApiPlClient(access_token=smsapi_access_token)
        smsreceiver = "+48" + request.POST['smsreceiver']
        smsmessage = request.POST['smsmessage']
        print(smsreceiver, smsmessage)
        client.sms.send(to=smsreceiver, message=smsmessage)

        return redirect('/smsapi/')