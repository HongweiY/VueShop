from django.shortcuts import render

from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .serializers import SmsSerializer, UserRegSerializer
from utils.yunpian import Yunpian
from VueShop.settings import YUNPIAN_API_KEY
from .models import VerifyCode

# Create your views here.

User = get_user_model()


class CustomBackends(ModelBackend):
    """
        自定义用户验证
        """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()
        yunpian = Yunpian(YUNPIAN_API_KEY)
        sms_status = yunpian.send_msg(mobile=mobile, code=code)
        if sms_status['code'] != 0:
            return Response({
                'name': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            verify_code = VerifyCode(mobile=mobile, code=code)
            verify_code.save()
            return Response({
                'name': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """"
    用户注册
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # 重载，返回token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 重载，返回user
        return serializer.save()
