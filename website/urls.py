from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Pages
    path('', views.index, name="index"),
    path('slider/', views.slider, name="slider"),
    path('smsapi/', views.smsapi, name="smsapi"),
    # polls
    path('polls/', views.polls, name="polls"),
    path('polls/createpoll/', views.createpoll, name="createpoll"),
    path('polls/results/<int:poll_id>', views.results, name="results"),
    path('polls/vote/<int:poll_id>', views.vote, name="vote"),
    # toDoLists
    path('todo', views.todo, name="todo"),
    path('todo/todolist/<int:todo_id>', views.todolist, name="todolist"),
    path('todo/createtodo/', views.createtodo, name="createtodo"),
    path("todo/todoedit/<int:todoitem_id>", views.todoedit, name="todoedit"),
    # Events
    path('sendsms/', views.sendsms, name="sendsms"),
    path("logout/", views.logout, name="logout"),
    path("addimage/", views.addimage, name="addimage"),
    path("deleteimage/", views.deleteimage, name="deleteimage"),
    path("deletetodo/<int:todo_id>", views.deletetodo, name="deletetodo"),
    path("deletetodoitem/<int:todoitem_id>", views.deletetodoitem, name="deletetodoitem"),
    path("itemcheck/<int:todoitem_id>", views.itemcheck, name="itemcheck"),
    path("itemuncheck/<int:todoitem_id>", views.itemuncheck, name="itemuncheck"),

    
    path("deletepoll/<int:poll_id>", views.deletepoll, name="deletepoll"),
    
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.STATICFILES_STORAGE, document_root=settings.STATICFILES_STORAGE)
