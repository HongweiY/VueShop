# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


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
