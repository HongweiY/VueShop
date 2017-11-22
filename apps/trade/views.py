from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.response import Response
from django.shortcuts import redirect

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from rest_framework.views import APIView
from utils.alipay import AliPay
from VueShop.settings import private_key_path, alipay_key_path
import datetime


# Create your views here.

class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    用户购物车
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()

        shop_cards = ShoppingCart.objects.filter(user=self.request.user)
        for shop_card in shop_cards:
            order_goods = OrderGoods()
            order_goods.goods = shop_card.goods
            order_goods.order = order
            order_goods.goods_num = shop_card.nums
            order_goods.save()

            shop_card.delete()
        return order


class AliPayView(APIView):
    def get(self, request):
        """
        处理同步返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016082500308985",
            app_notify_url="http://45.77.220.209:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://45.77.220.209:8001/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            response = redirect('index')
            return response

    def post(self, request):
        """
        处理一步请求
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016082500308985",
            app_notify_url="http://45.77.220.209:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://45.77.220.209:8001/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
