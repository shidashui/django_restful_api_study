"""api_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from api_study.settings import MEDIA_ROOT
from goods.views import GoodsListView, GoodsListViewSet, CategoryViewSet
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet, base_name="categorys")
#users
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")
#user_operation
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'messages', LeavingMessageViewset, base_name="messages")
router.register(r'address', AddressViewset, base_name="address")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/',include('DjangoUeditor.urls')),
    path('api-auth/', include('rest_framework.urls')),
    #文件
    path('media/<path:path>', serve, {'document_root':MEDIA_ROOT}),
    #drf文档， title自定义
    path('docs', include_docs_urls(title='docs for test')),
    #token
    path('api-token-auth/', views.obtain_auth_token),
    #jwt的token认证接口
    path('login/', obtain_jwt_token),

    #商品列表页
    re_path('^', include(router.urls)),
    # path('goods/', GoodsListView.as_view(), name='goods-list'),
]
