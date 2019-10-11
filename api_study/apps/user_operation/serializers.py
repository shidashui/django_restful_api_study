from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator


class UserFavSerializer(serializers.ModelSerializer):
    #获取当前登陆用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        #validate实现联合唯一， 一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                #message的消息可以自定义
                message="已经收藏",
            ),
        ]
        model = UserFav
        #收藏的时候需要返回商品的id，因为取消收藏时必须知道商品的id
        fields = ("user", "goods", "id")