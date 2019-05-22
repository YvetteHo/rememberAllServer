from django.shortcuts import render
from .models import Note, File
from rest_framework import viewsets
from .serializer import NoteSerializer, UserSerializer, FileSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
import datetime


from rest_framework.decorators import action
# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            print(serializer.errors)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        serializer = NoteSerializer(data=request_data)
        print(serializer)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': 'success'})
        else:
            print(serializer.errors)
            return Response({'status': 'fail'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=True)
    def login(self, request, pk=None):
        request_data = request.data
        if User.objects.filter(username=request_data['username']).exists():
            user = User.objects.get(username=request_data['username'])
            if user.check_password(request_data['password']):
                token = Token.objects.create(user=user)
                return Response({'status': 'success', 'token': str(token)})
            else:
                return Response({'status': 'fail', 'message': '用户名或密码错误'})
        else:
            return Response({'status': 'fail', 'message': '用户名不存在'})

    @action(methods=['post'], detail=True)
    def logout(self, request, pk=None):
        request_data = request.data
        print('delete')
        user = User.objects.get(username=request_data['username'])
        user.auth_token.delete()
        return Response({'status': 'success'})

    def create(self, request, *args, **kwargs):
        request_data = request.data
        if User.objects.filter(username=request_data['username']).exists():
            return Response({'status': 'fail', 'message': '用户名已存在，请更换'})
        else:
            user = User.objects.create_user(username=request_data['username'], password=request_data['password'])
            token = Token.objects.create(user=user)
            return Response({'status': 'success', 'token': str(token)})

    def list(self, request, *args, **kwargs):
        if 'Username' in request.headers:
            user_name = request.headers['Username']
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=user_name)

            notes = user.notes.all()
            serializer = NoteSerializer(notes, many=True, context={'request': self.request})
            return Response(serializer.data)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True, context={'request': self.request})
            return Response(serializer.data)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # parser_classes = (FileUploadParser,)

    def create(self, request, *args, **kwargs):
        new_data = request.data
        new_data['timestamp'] = datetime.datetime.now()

        file_serializer = FileSerializer(data=new_data)
        if file_serializer.is_valid():

            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(file_serializer.data)

            print(file_serializer.errors)

            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
    #     # do some stuff with uploaded file
    #     return Response(status=204)
# class FileView(views.APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         file_serializer = FileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

