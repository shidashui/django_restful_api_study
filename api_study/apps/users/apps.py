from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    #app名字后台中文显示
    verbose_name = "用户管理"