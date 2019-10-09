from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from goods.serializers import GoodsSerializer
from .models import Goods
from rest_framework.response import Response


# class GoodsListView(APIView):
#     """
#     商品列表
#     """
#     def get(self,request,format=None):
#         goods = Goods.objects.all()
#         goods_serialzer = GoodsSerializer(goods, many=True)
#         return Response(goods_serialzer.data)

#自定义分页
class GoodsPagination(PageNumberPagination):
    """
    商品列表自定义分页
    """
    page_size = 10                      #默认每页显示个数
    page_size_query_param = 'page_size' #可以动态改变每页显示的个数，在url
    page_query_param = 'page'           #页码参数
    max_page_size = 100                 #最多显示多少页

class GoodsListView(generics.ListAPIView):
    pagination_class = GoodsPagination  #分页
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表分页
    """
    pagination_class = GoodsPagination
    #这里必须要定义一个默认的排序，否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer