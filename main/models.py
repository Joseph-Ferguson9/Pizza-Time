from django.db import models
import re

from django.http import request

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
# Create your models here.

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors["f_name"] = "Submitted first name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors["l_name"] = "Submitted last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        users_with_email = Users.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists"
        if len(postData['address']) < 5:
            errors['address'] = "Address must be more than 5 characters"
        if len(postData['city']) < 2:
            errors['city'] = "City must be more than 2 characters"
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must be between 8 and 20 characters, contain at least one digit, one uppercase, one lowercase, and one special character"
        if postData['password'] != postData['confirm_pw']:
            errors['pw_match'] = "Passwords must match"
        return errors
    def user_update_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors["f_name"] = "Submitted first name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors["l_name"] = "Submitted last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['address']) < 5:
            errors['address'] = "Address must be more than 5 characters"
        if len(postData['city']) < 2:
            errors['city'] = "City must be more than 2 characters"
        return errors

class Users(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=75)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()