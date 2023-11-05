from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    emailid = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  # You may consider using a PasswordField
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    delete_flag = models.BooleanField(default=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    delete_flag = models.BooleanField(default=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)

class Role(models.Model):
    role_name = models.CharField(max_length=50)
    delete_flag = models.BooleanField(default=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)
