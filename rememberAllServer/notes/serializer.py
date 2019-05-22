from rest_framework import serializers
from .models import Note, File
from django.contrib.auth.models import User


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name', 'time', 'noteType', 'noteContent', 'noteSkeleton', 'user')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'note')

