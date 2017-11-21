# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from goods.models import Goods


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车
    """
    # 设置当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(min_value=1, required=True, error_messages={
        'min_value': '最少购买一件',
        'required': '最少购买一件'
    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed_shop_cart = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed_shop_cart:
            existed_shop_cart = existed_shop_cart[0]
            existed_shop_cart.nums += nums
            existed_shop_cart.save()
        else:
            existed_shop_cart = ShoppingCart.objects.create(**validated_data)

        return existed_shop_cart

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号
        import time
        from random import Random
        order_sn = '{time_str}{user_id}{ran_str}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                         user_id=self.context['request'].user.id,
                                                         ran_str=Random().randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
