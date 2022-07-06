from django.shortcuts import render
from .models import Image

# site Pages
def index(request):
    return render(request, 'index.html')

def slider(request):
    image_object = Image.objects.all()
    context = {
        'images': image_object, 
    }
    print(image_object)
    return render(request, 'slider.html', context)

# Events

# 404 Handling
def view_page_not_found(request, exception):
    return render(request, '404.html')