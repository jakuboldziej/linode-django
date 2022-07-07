from django.db import models

class Image(models.Model):
    img_src = models.FileField(upload_to="slider_images")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class TwoOptionPoll(models.Model):
    question = models.TextField(max_length=100)
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count

    def __str__(self):
        return self.question
    