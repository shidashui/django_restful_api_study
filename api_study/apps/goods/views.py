# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from goods.filters import GoodsFilter
from goods.models import GoodsCategory
from goods.serializers import GoodsSerializer, CategorySerializer
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
    page_size = 12                      #默认每页显示个数
    page_size_query_param = 'page_size' #可以动态改变每页显示的个数，在url
    page_query_param = 'page'           #页码参数
    max_page_size = 100                 #最多显示多少页

class GoodsListView(generics.ListAPIView):
    pagination_class = GoodsPagination  #分页
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin ,viewsets.GenericViewSet):
    """
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    """
    pagination_class = GoodsPagination
    #这里必须要定义一个默认的排序，否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 设置filter的类为我们自定义的类
    # 过滤
    filter_class = GoodsFilter
    # 排序
    ordering_fields = ('sold_num', 'shop_price')
    # 搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer