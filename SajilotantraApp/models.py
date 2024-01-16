from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from Sajilotantra import settings

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     fName = models.CharField(max_length=200)
#     lName = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     image = models.ImageField(upload_to='static/profiles/', null=True, blank=True)
#     bio = models.CharField(max_length=255, null=True, blank=True)
#     # image = models.ImageField()

#     def __str__(self):
#         return self.user_id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images/', null=True, blank=True)
    cover = models.ImageField(upload_to='static/cover_images/', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username

class GovernmentProfile(models.Model):
    profile_id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    description = RichTextField() 
    address = models.CharField(max_length=200)

class Guidance(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = RichTextField() 
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    notice_id=models.AutoField(primary_key=True)
    notice_title=models.CharField(max_length=500)
    notice_description=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)
    posted_by=models.CharField(max_length=200)

    def __str__(self):
        return self.notice_title

    
class Event(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField()
    start=models.DateTimeField(null=True,blank=True)
    end=models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    category = models.CharField(max_length=100)
    suggestion = models.TextField()

class UploadedFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    file = models.FileField(upload_to='static/feedback_files/')

    def __str__(self):
        return self.file.name
    
    

class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.TextField()
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    # date_posted=models.DateTimeField(auto_now_add=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# models.py
from django.db import models

class ReportedPost(models.Model):
    post_id = models.CharField(max_length=255, unique=True)
    post = models.FileField(upload_to='uploaded_files/')

    def __str__(self):
        return f"Reported Post {self.post_id}"


