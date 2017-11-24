# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserFav


@receiver(post_save, sender=UserFav)
def create_User_fav(sender, instance=None, created=False, **kwargs):
    # 采用Django信号量，更改用户收藏量
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_User_fav(sender, instance=None, created=False, **kwargs):
    # 采用Django信号量，更改用户收藏量
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
