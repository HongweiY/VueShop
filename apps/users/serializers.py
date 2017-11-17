# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from VueShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("请输入合法手机号")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, help_text='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, )
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_code:
            last_verify_code = verify_code[0]
            # 验证码过期时间5分钟
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_verify_code.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')

            if last_verify_code.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
