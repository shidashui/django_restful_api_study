from django.views.generic import View
from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        #通过django的view实现商品列表页
        json_list = []
        goods = Goods.objects.all()
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)

        from django.http import HttpResponse    #这个样子性能好，需要时导入
        import json
        from django.core import serializers
        from django.http import JsonResponse

        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        #返回json，必须指定类型content_type = 'application/json'
        # return HttpResponse(json.dumps(json_list), content_type='application/json')
        return JsonResponse(json_data, safe=False)

