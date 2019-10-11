from rest_framework import serializers

from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage
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

class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情
    """
    #通过商品id获取收藏的商品， 需要嵌套商品的序列化
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言
    """
    #获取当前登陆的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #read_only：只返回，post时候可以不用提交，format：格式化输出
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")
