from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
import sys
# Create your models here.
from django import forms


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=5)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.id


class Note(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=5)
    time = models.DateTimeField(default=now)
    noteType = models.CharField(max_length=10)
    noteContent = models.CharField(max_length=sys.maxsize)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.id




