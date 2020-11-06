from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters!"
        if len(postdata['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be valid format!"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters!"
        if postdata['password'] != postdata['conf_password']:
            errors['conf_password']="Password and confirm password must match!"
        return errors
    def login_validator(self, postdata):
        errors = {}
        check = User.objects.filter(email=postdata['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postdata['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class BookManager(models.Manager):
    def book_validator(self, postdata):
        errors={}
        if len(postdata['title'])<2:
            errors['title']="Title must be at least two characters long!"
        if len(postdata['desc'])<8:
            errors['desc']="Description must be at least eight characters long!"
        return errors

class Book(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    person = models.ForeignKey(User, related_name='user_book', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=BookManager()