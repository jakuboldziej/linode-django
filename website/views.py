from django.shortcuts import render

def index(requset):
    return render(requset, 'index.html')

def view_page_not_found(request, exception):
    return render(request, '404.html')