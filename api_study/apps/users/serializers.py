import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

from api_study.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    #函数名必须：validate+验证字段名
    def validate_mobile(self, mobile):
        """
        手机号验证
        :param mobile:
        :return:mobile
        """
        #是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        #是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        #验证码发送频率，60s一次
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''
    #UserProfile中没有code字段，这里需要自定义一个code序列话字段
    code = serializers.CharField(required=True, write_only=True, max_length=4,min_length=4,
                                 error_messages={
                                     "blank":"请输入验证码",
                                     "requried":"请输入验证码",
                                     "max_length":"验证码格式错误",
                                     "min_length":"验证码格式错误"
                                 }, help_text="验证码")
    #验证用户名是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    #输入密码时不显示明文
    password = serializers.CharField(style={'input_type':'password'}, label='密码', write_only=True)

    #验证code
    def validate_code(self, code):
        #用户注册， 以post方式提交注册信息，post的数据都保存至initial_data里面
        #username就是用户注册的手机号， 验证码按添加时间倒序排序，为了后面验证过去，错误等
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        if verify_records:
            last_records = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)     #有效期5分钟
            if five_mintes_ago > last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    #所有字段. attrs是字段验证合法之后返回的总dict
    def validate(self, attrs):
        #前端没有传mobile值到后端，这里添加进来
        attrs["mobile"] = attrs["username"]
        #code是自己添加的，数据库没有这个字段，验证完就删除
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')


