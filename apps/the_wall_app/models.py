from django.db import models
import re
from datetime import datetime

def diff_month(d1, d2) :
    return (d2.year - d1.year) * 12 + d2.month - d1.month
    
# Create your models here.
class UserManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        first_name = postData['first_name']
        # first name & last_anme >=2 characters
        if (len(first_name) == 0) :
            errors['first_name'] = "First name is required"
        elif (len(first_name) < 2) :
            errors['first_name'] = "First name should be at least 2 characters"

        last_name = postData['last_name']
        if (len(last_name) == 0) :
            errors['last_name'] = "Last name is required"
        elif (len(last_name) < 2) :
            errors['last_name'] = "Last name should be at least 2 characters"

        # email should be valid
        email = postData['email']
        if (len(email) == 0) :
            errors['email'] = "Email is required"
        else :
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-z]+$')
            if not EMAIL_REGEX.match(email) :
                errors['email'] = "Email should be valid"
            else : # check uniqueness
                users = User.objects.filter(email=email)
                if (len(users) > 0) :
                    errors['email'] = "Email already exists!"

        # Birthday validation (in the past)
        bday = postData['bday']
        # print("***bday: ", bday,len(bday))
        if (len(bday) == 0) :
            errors['bday'] = "Birthday is required"
        else :
            try :
                bday = datetime.strptime(bday, '%Y-%m-%d')
                print (bday, datetime.now())
                if (bday >= datetime.now()) :
                    errors['bday'] = "Birthday should be a date in the past"
                elif (diff_month(bday, datetime.now()) < 12 * 13):
                # elif (relativedelta(datetime.now()-bday).years < 13) :
                    errors['bday'] = "User should be at least 13 years old to register"
            except :
                errors['bday'] = "Birthday should be a valid date"

        # password should be at least 8 characters
        password = postData['password']
        if (len(password) < 8) :
            errors['password'] = "Password should be at least 8 characters"
        
            # hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        else :
            # password should match
            confirm_pw = postData['confirm_password']
            if (not password == confirm_pw) :
                errors['confirm_password'] = "Password should match!"

        return errors

class User(models.Model) :
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessageManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        # content
        content = postData['message']
        if (len(content) < 5) :
            errors['message'] = "Message should contain at least 5 characters"
        
        return errors

class Message(models.Model) :
    content = models.TextField()
    user = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        # content
        content = postData['comment']
        if (len(content) < 5) :
            errors['comment'] = "Comment should contain at least 5 characters"
        
        return errors

class Comment(models.Model) :
    content = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()