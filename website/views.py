from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User, auth

from .forms import RegisterForm
from .models import Image, TwoOptionPoll, Message, ToDoList, ToDoListItem

from smsapi.client import SmsApiPlClient

smsapi_access_token = 'L3LlVvkfevSgw0wqeADhLEYLkc6Z27FCzrGm9aeH'

# Pages
def index(request):
    users = User.objects.all()
    images = Image.objects.all()
    polls = TwoOptionPoll.objects.all()
    todoLists = ToDoList.objects.all()

    context = {
        'users': users,
        'images': images,
        'polls': polls,
        'todoLists': todoLists,
    }
    return render(request, 'index.html', context)

def slider(request):
    image_object = Image.objects.all()
    context = {
        'images': image_object, 
    }
    return render(request, 'slider.html', context)

def smsapi(request):
    SMS = Message.objects.all()
    context = {
        'SMS': SMS,
    }

    return render(request, 'smsapi.html', context)
        
def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect("/login")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})

# ToDoLists
def todo(request):
    if request.user.is_authenticated:
        todoList = ToDoList.objects.filter(user=request.user)

        context = {
            "todoLists": todoList,
        }
        return render(request, 'todo.html', context)
    else:
        return render(request, 'todo.html')

def todolist(request, todo_id):
    todoList = ToDoList.objects.get(id=todo_id)
    todoListItem = ToDoListItem.objects.filter(todolist=todoList)
    if request.method == 'POST':
        if 'todoTitle' in request.POST:
            todoTitle = request.POST['todoTitle']
            todoListItemSave = ToDoListItem.objects.create(todolist=todoList, title=todoTitle)
            todoListItemSave.save()

            print("Created todo item " + todoTitle)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        request.session['current_todolist'] = todo_id
        request.session.modified = True

        todoListItem_checked = ToDoListItem.objects.filter(todolist=todoList, checked=True).count()

        context = {
            'todoList': todoList,
            'todoListItems': todoListItem,
            'todoListItem_checked': todoListItem_checked,
        }
        return render(request, 'todolist.html', context)

def createtodo(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        todotitle = request.POST['todotitle']

        new_todoList = ToDoList.objects.create(user=user, title=todotitle)
        new_todoList.save()

        return redirect('todo')
    else:
        return render(request, 'createtodo.html')

def todoedit(request, todoitem_id):
    current_todolist = request.session['current_todolist']
    todoListItem = ToDoListItem.objects.get(id=todoitem_id)
    todoList = ToDoList.objects.get(id=current_todolist)
    
    if request.method == 'POST':
        print("POST")
        todoListItem.title = request.POST['todoItemTitle']
        todoListItem.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        context = {
            'todoListItem': todoListItem,
            'todolist_id': current_todolist,
            'todoList': todoList,
        }
        print("openeded without post")
        return render(request, 'todoedit.html', context) 

# Polls

def createpoll(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        question = request.POST['question']
        option_one = request.POST['optionone']
        option_two = request.POST['optiontwo']

        new_poll = TwoOptionPoll.objects.create(user=user, question=question, option_one=option_one, option_two=option_two)
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

# 404 Handling
def view_page_not_found(request, exception):
    return render(request, '404.html')

# Events

def addimage(request):
    if request.method == 'POST':
        img_src = request.FILES.getlist('image')
        for img in img_src:
            print(img)
            img = Image.objects.create(img_src=img, title=img)
            img.save()
    
    return redirect('slider')

def deletetodo(request, todo_id):
    todoList = ToDoList.objects.get(id=todo_id)
    todoList.delete()

    return redirect('todo')

def deletetodoitem(request, todoitem_id):
    todoListItem = ToDoListItem.objects.get(id=todoitem_id)

    todoListItem.delete()

    return redirect(request.META.get('HTTP_REFERER'))   

def itemcheck(request, todoitem_id):
    todoListItem = ToDoListItem.objects.get(id=todoitem_id)
    todoListItem.checked = True
    todoListItem.save()

    return redirect(request.META.get('HTTP_REFERER'))

def itemuncheck(request, todoitem_id):
    todoListItem = ToDoListItem.objects.get(id=todoitem_id)
    todoListItem.checked = False
    todoListItem.save()

    return redirect(request.META.get('HTTP_REFERER'))

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
    return redirect('todo')

def logout(request):
    auth.logout(request)
    return redirect('/')

def sendsms(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user.username
            client = SmsApiPlClient(access_token=smsapi_access_token)
            smsreceiver = "+48" + request.POST['smsreceiver']
            smsmessage = request.POST['smsmessage']
            print(smsreceiver, smsmessage)
            client.sms.send(to=smsreceiver, message=smsmessage)
            SMS = Message.objects.create(user=user, phoneNumber=smsreceiver, message=smsmessage, date=date.now())
            SMS.save()

            return redirect('/smsapi/')
    else:
        messages.add_message(request, messages.INFO, 'You have to be logged in to vote')
        return redirect('/smsapi/')
