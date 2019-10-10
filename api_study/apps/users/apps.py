from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    #app名字后台中文显示
    verbose_name = "用户管理"

    #重载配置
    def ready(self):
        import users.signals