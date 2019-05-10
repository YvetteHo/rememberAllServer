from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
import sys
# Create your models here.
from django import forms


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=5)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.id


class Note(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=5, blank=True)
    time = models.DateTimeField(default=now)
    noteType = models.CharField(max_length=10, blank=True)
    noteContent = models.CharField(max_length=sys.maxsize, default='[]')
    noteSkeleton = models.CharField(max_length=sys.maxsize, default='[]')
    user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class File(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note, related_name='files', on_delete=models.CASCADE)
