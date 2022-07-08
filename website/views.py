from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User, auth

from .forms import RegisterForm
from .models import Image, TwoOptionPoll
from datetime import date

from smsapi.client import SmsApiPlClient

smsapi_access_token = 'L3LlVvkfevSgw0wqeADhLEYLkc6Z27FCzrGm9aeH'

# Pages
def index(request):
    return render(request, 'index.html')

def slider(request):
    image_object = Image.objects.all()
    context = {
        'images': image_object, 
    }
    return render(request, 'slider.html', context)

def smsapi(request):
    return render(request, 'smsapi.html')
        
def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect("/login")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})

# 404 Handling
def view_page_not_found(request, exception):
    return render(request, '404.html')

def createpoll(request):
    if request.method == 'POST':
        user_object = User.objects.get(username=request.user.username)
        question = request.POST['question']
        option_one = request.POST['optionone']
        option_two = request.POST['optiontwo']

        new_poll = TwoOptionPoll.objects.create(user=user_object, question=question, option_one=option_one, option_two=option_two)
        new_poll.save()
        return redirect('polls')
    else:
        return render(request, 'createpoll.html')

def polls(request):
    try:
        poll_object = TwoOptionPoll.objects.all()
        context ={
            'polls': poll_object,
        }
        return render(request, 'polls.html', context)
    except:
        return render(request, 'polls.html')

def vote(request, poll_id):
    poll = TwoOptionPoll.objects.get(id=poll_id)

    if poll.user_votes is None:
        poll.user_votes = ""
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_list_split = poll.user_votes.split(", ")[:-1]

            user_list = [user[:-1] for user in user_list_split]
        
            try:
                selected_option = request.POST['option']
            except:
                selected_option = None
                poll.user_votes = None
            if request.user.username in user_list:
                messages.add_message(request, messages.INFO, 'You cannot vote twice')
            else:
                if selected_option == None:
                    pass
                else:
                    if selected_option == 'option1':
                        poll.option_one_count += 1
                        poll.user_votes += request.user.username + "1" + ", "
                    elif selected_option == 'option2':
                        poll.option_two_count += 1
                        poll.user_votes += request.user.username + "2" + ", "

            poll.save()
            return redirect('polls')
        else:
            user_list_split = poll.user_votes.split(", ")[:-1]
            user_dict = dict()
            for user in user_list_split:
                user_dict[user[:-1]] = user[-1]
            
            user_dict_copy = user_dict.copy()
            for user in user_dict_copy:
                if user != request.user.username:
                    del user_dict[user]

            user_voted_on = list(user_dict.values())
            
            if user_voted_on != []:
                user_voted_on = int(user_voted_on[0])
            context = {'poll': poll, 'user_voted_on': user_voted_on}

            return render(request, 'vote.html', context)
    messages.add_message(request, messages.INFO, 'You have to be logged in to vote')
    
    return redirect('polls')
    
def results(request, poll_id):
    poll = TwoOptionPoll.objects.get(id=poll_id)

    user_votes_list = poll.user_votes
    option1_list = []
    option2_list = []
    
    if user_votes_list is not None:
        user_list = user_votes_list.split(", ")[:-1]
        for user in user_list:
            if user[-1] == "1":
                option1_list.append(user[:-1])
            else:
                option2_list.append(user[:-1])

    context ={
        'poll': poll,
        'option1_list': option1_list,
        'option2_list': option2_list,
        'user_votes_list': user_votes_list,
    }
    return render(request, 'results.html', context)

# Events

def addimage(request):
    if request.method == 'POST':
        img_src = request.FILES.getlist('image')
        for img in img_src:
            img = Image.objects.create(img_src=img, title="asdf")
            img.save()
    
    return redirect('slider')

def deleteimage(request):
    if request.method == 'POST':
        img_src = request.POST.get('img_src')
        if img_src is not None:
            img_obj = Image.objects.get(img_src=img_src)
            img_obj.delete()
        else:
            return redirect('slider')        

    return redirect('slider')

def deletepoll(request, poll_id):
    poll = TwoOptionPoll.objects.get(id=poll_id)
    poll.delete()
    return redirect('polls')

def logout(request):
    auth.logout(request)
    return redirect('/')

def sendsms(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            client = SmsApiPlClient(access_token=smsapi_access_token)
            smsreceiver = "+48" + request.POST['smsreceiver']
            smsmessage = request.POST['smsmessage']
            print(smsreceiver, smsmessage)
            client.sms.send(to=smsreceiver, message=smsmessage)

            return redirect('/smsapi/')
    else:
        messages.add_message(request, messages.INFO, 'You have to be logged in to vote')
        return redirect('/smsapi/')
