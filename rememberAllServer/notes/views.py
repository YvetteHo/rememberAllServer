from django.shortcuts import render
from .models import Note, User, File
from rest_framework import viewsets, views
from rest_framework.request import Request
from rest_framework.parsers import FileUploadParser
from .serializer import NoteSerializer, UserSerializer, FileSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
import uuid
from rest_framework.decorators import action
# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        # 如果是笔记
        if request_data['id'] == '':
            new_id = str(uuid.uuid1())
            request_data['id'] = new_id
            # request_data['user'] = User.objects.get(pk=request_data['user'])
            serializer = NoteSerializer(data=request_data)
            print(serializer)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'status': 'success', 'noteId': new_id})
            else:
                print(serializer.errors)
                return Response({'status': 'fail'})

        else:
            return Response('喵喵喵')
    #

    # def retrieve(self, request, *args, **kwargs):
    #     # print(request.Meta)
    #     # queryset = self.get_queryset()
    #     queryset = Note.objects.all()
    #
    #     serializer = NoteSerializer(queryset, many=True)
    #     return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        # 如果是新用户
        if request_data['id'] == '':
            new_id = str(uuid.uuid1())
            request_data['id'] = new_id
            serializer = UserSerializer(data=request_data)
            print(serializer)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'status': 'success', 'userId': new_id})
            else:
                print(serializer.errors)
                return Response({'status': 'fail'})
            # 如果是老用户登陆
        else:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=request_data['id'])
            serializer = UserSerializer(user)
            if request_data['name'] == serializer.data['name'] and request_data['password'] == serializer.data['password']:
                return Response('success')
            else:
                return Response('fail')

    # @action(detail=True, methods=['post'])
    # def create_user(self, request, pk=None):
    #     print('被调用啦')
    #     return Response('mmm')
        # serializer = NoteSerializer(data=request.data)
        # if serializer.is_valid():
        #     user_id = serializer.id
        #     if user_id == '':
        #         new_id = uuid.uuid1()
        #         serializer.id = new_id
        #         self.perform_create(serializer)
        #         return Response({'status': 'successfully login', 'userId': new_id})
        #     else:
        #         queryset = User.objects.all()
        #         user = get_object_or_404(queryset, pk=user_id)
        #         if serializer.name == user.name and serializer.password == user.password:
        #             return Response({'status': 'successfully login'})
        #         else:
        #             return Response({'status': 'wrong user id or password'})

    def list(self, request, *args, **kwargs):
        print('不太对吧')
        # queryset = User.notes.all()
        # serializer = UserSerializer(queryset, many=True)
        # return Response(serializer.data)
        # print(self.request.headers)
        # print('get', self.request.GET.get('id'))
        if 'Userid' in request.headers:
            user_id = request.headers['Userid']
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=user_id)

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
        file_serializer = FileSerializer(data=request.data)
        print(request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
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

