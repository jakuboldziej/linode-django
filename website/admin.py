from django.contrib import admin
from .models import Image, TwoOptionPoll, Message, ToDoList, ToDoListItem

admin.site.register(Image)
admin.site.register(Message)

@admin.register(TwoOptionPoll)
class TwoOptionPollAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_one', 'option_two', 'user')
    ordering = ('user',)
    search_fields = ('question',)

@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    ordering = ('user',)
    search_fields = ('title',)

@admin.register(ToDoListItem)
class ToDoListItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'todolist', 'checked')
    ordering = ('todolist',)
    search_fields = ('title',)