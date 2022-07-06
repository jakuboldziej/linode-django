from django.db import models

class Image(models.Model):
    img_src = models.ImageField(upload_to="slider_images")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title