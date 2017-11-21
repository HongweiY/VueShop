# -*- coding: utf-8 -*-
__author__ = 'ymfsder'
import re

from rest_framework import serializers
from .models import ShoppingCart
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
