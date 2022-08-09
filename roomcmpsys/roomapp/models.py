from tkinter import CASCADE
from django.db.models import F
from tkinter.tix import Tree
from turtle import mode
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from numpy import save
from .choices import ATTENDED_CHOICE, BLOCKS, CATEGORY_CHOICE, ROOM_NO, GENDER, HOSTEL_NAMES




class Hostel(models.Model):
    name = models.CharField(max_length=100, choices= HOSTEL_NAMES)
    gender = models.CharField(max_length=100, choices=GENDER)
    block = models.CharField(max_length=100, choices=BLOCKS)
    room_no = models.CharField(max_length=100, choices=ROOM_NO)
    
    
    def __str__(self):
        return f"{self.name + ' ' + self.gender + '-'+' Block ' + self.block + ' '+' Room '  + self.room_no}"





class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)  
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    is_supervisor = models.BooleanField(default=False, verbose_name='Supervisor')
    is_student = models.BooleanField(default=False, verbose_name='Student')
    hostel = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.CASCADE)
    
    
    USERNAME_FIELD = 'username'
    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Complain(models.Model):
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE, default='PLUMBING')
    subject = models.CharField(max_length=100)
    complain_start_date = models.DateField(blank=True)
    date_reported = models.DateField(default=timezone.now)
    desc = models.CharField(max_length=200)
    is_attended =models.CharField(max_length=100, choices=ATTENDED_CHOICE, default='NO')
    hostel = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank = True, on_delete=models.CASCADE)
    
    date_reported.editable = True
    def __str__(self):
        return self.desc


    def get_absolute_url(self):
        return reverse("complaint", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        return super(Complain, self).save(*args, **kwargs)




