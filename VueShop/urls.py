"""VueShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

import xadmin
from VueShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryListViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet

router = DefaultRouter()

# 配置商品的URL
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置商品分类的URL
router.register(r'categories', CategoryListViewSet, base_name='categories')
# 短信呢验证码
router.register(r'code', SmsCodeViewSet, base_name='code')
# 用户注册
router.register(r'users', UserViewSet, base_name='user')
# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register(r'messages', LeavingMessageViewSet, base_name='messages')

# 用户收货地址
router.register(r'address', UserAddressViewSet, base_name='address')

# 用户购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'docs/', include_docs_urls(title='ymfsder')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt认证接口
    url(r'^login/', obtain_jwt_token),
]
