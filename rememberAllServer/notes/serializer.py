from rest_framework import serializers
from .models import Note, User, File


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name', 'time', 'noteType', 'noteContent', 'noteSkeleton', 'user')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'remark', 'timestamp', 'note')

