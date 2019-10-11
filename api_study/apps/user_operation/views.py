from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.

class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    用户收藏
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
