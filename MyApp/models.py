from django.db import models
from django.contrib.auth.models import  User
import uuid
import os


# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars', filename)

class Teacher(models.Model):
    first_name = models.CharField(null=True, max_length = 30)
    last_name = models.CharField(null=True, max_length = 30 )
    def __str__(self):
        return self.first_name + " " + self.last_name


class Cours(models.Model):
    name = models.CharField(null=True, max_length = 100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null = True)
    def __str__(self):
        return self.name


class student(models.Model):
    first_name = models.CharField(null=True, max_length = 30)
    last_name = models.CharField(null=True, max_length = 30)
    room = models.CharField(null=True, max_length = 255)
    email = models.EmailField(null=True)
    discription = models.TextField(default="")
    cours = models.ForeignKey(Cours, on_delete=models.SET_NULL, null = True)
    photo = models.FileField(upload_to='avatars',null=True, default=None, max_length=100)
    def __str__(self):
        return self.first_name + " " + self.last_name


class Comment(models.Model):
    user_for = models.ForeignKey(student, on_delete=models.SET_NULL, null = True)
    user_from = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    text = models.TextField(null=True)

class Ticket(models.Model):
    student_for = models.ForeignKey(student, on_delete=models.SET_NULL,null=True)
    user_from = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    data = models.DateField()
    is_it = models.BooleanField(default = False)


