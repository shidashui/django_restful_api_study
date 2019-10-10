import django_filters

from .models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤的类
    """
    #两个参数，name是要过滤的字段，lookup是执行的行为，’小于等于本地价格‘
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    top_category = django_filters.NumberFilter(name="category", method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        #不管当前点击的是一级分类还是二级三级，都能找到
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']