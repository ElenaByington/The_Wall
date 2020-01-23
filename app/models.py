from django.db import models
from datetime import date, datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self,dataPost):
        errors = {}
        print(dataPost)
        if len(dataPost['first_name']) < 2:
            errors['first_name'] = "First name must have 2 and more characters."
        if len(dataPost['last_name']) < 2:
            errors['last_name'] = "Last name must have 2 and more characters."
        # if dataPost['bday']=="":
        #     errors['bday']="Birthday cannot be empty"
        # else:
        #     if datetime.today()<datetime.strptime(dataPost['bday'], '%Y-%M-%d'):
        #         errors['bday']="No dates in the future"
        if not EMAIL_REGEX.match(dataPost['email']):
            errors['email'] = "Email is invalid."
        if User.objects.filter(email=dataPost['email']).exists():
            errors['email'] = "Email already exists, try logging in."
        # if len(dataPost['bio'])>100:
        #     errors['bio']="Bio too long"
        if dataPost['password'] == "":
            errors['password'] = "Password must have 8 or more characters."
        if dataPost['password'] != dataPost['confirm_password']:
            errors['confirm_pass'] = "Passwords do not match."
        return errors

    def login_validator(self,dataPost):
        errors = {}
        print(dataPost)
        if not EMAIL_REGEX.match(dataPost['email']):
            errors['email'] = "Invalid credentials."
        if dataPost['password'] == "":
            errors['password'] = "Invalid credentials."
        return errors

class PostMessageManager(models.Manager):
    def postmessage_validator(self,dataPost):
        errors = {}
        print(dataPost)
        if len(dataPost['postmessage']) < 10:
            errors['postmessage'] = "Message must have 10 or more characters."
        return errors

class CommentManager(models.Manager):
    def comment_validator(self,dataPost):
        errors = {}
        print(dataPost)
        if len(dataPost['comment']) < 10:
            errors['comment'] = "Comment must have 10 or more characters."
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"<User Object: {self.id} {self.first_name} {self.last_name}>"

class PostMessage(models.Model):
    posted_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user_message = models.ForeignKey(User, related_name="posted_messages", on_delete = models.CASCADE)
    objects = PostMessageManager()

    def __repr__(self):
        return f"<User Object: {self.id} {self.posted_message}>"

class Comment(models.Model):
    posted_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    posted_message = models.ForeignKey(PostMessage, related_name="message_comments", on_delete = models.CASCADE)
    user_comment = models.ForeignKey(User, related_name="user_comments", on_delete = models.CASCADE)
    objects = CommentManager()

    def __repr__(self):
        return f"<User Object: {self.id} {self.posted_comment}>"
