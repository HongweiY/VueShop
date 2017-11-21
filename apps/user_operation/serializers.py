# -*- coding: utf-8 -*-
__author__ = 'ymfsder'
import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer
from VueShop.settings import REGEX_MOBILE


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏
    """
    # 设置当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='您已经收藏过该商品'
            )
        ]
        fields = ('user', 'goods', 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言
    """
    # 设置当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class UserAddressSerializer(serializers.ModelSerializer):
    """"
    用户收货地址
    """
    # 设置当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'add_time')
