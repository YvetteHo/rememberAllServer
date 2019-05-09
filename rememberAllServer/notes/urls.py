from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, UserViewSet, FileViewSet
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

# from . import views
router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'users', UserViewSet)
router.register(r'files', FileViewSet)

swagger_view = get_swagger_view(title='rememberAll API')

urlpatterns = [
    path('', include(router.urls)),
    # path('\', get_swagger_view(title="API"))

    path('api/', swagger_view, name='api'),
    path('api-auth/', include('rest_framework.urls')),
    # path('upload/', FileView.as_view(), name='file-upload'),
]