from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + "\n" + self.description
    
class Report(models.Model):
    Name = models.CharField(max_length=200)
    Brand = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    Category = models.CharField(max_length=200)
    description = models.TextField()
    date_created= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_link = models.URLField(null=True)
    is_resolved = models.BooleanField(default=False)
    def __str__(self):
        return self.Name + "\n" + self.description
    def save(self, *args, **kwargs):
        if self.pk is not None:  # the report has been saved before
            self.date_updated = timezone.now()
        super().save(*args, **kwargs)


'''
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
'''