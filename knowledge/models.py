from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)


class Post(models.Model):
    title=models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Knowledge(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE,related_name='knowledges')
    tags=models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    knowledge=models.ForeignKey(Knowledge, on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.text[:20]
    

