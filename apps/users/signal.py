# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 采用Django信号量，加密用户密码
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
