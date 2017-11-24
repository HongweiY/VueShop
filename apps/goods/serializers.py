# -*- coding: utf-8 -*-
__author__ = 'ymfsder'

from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd
from django.db.models import Q


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = ('__all__')


class HotSearchWordsSerializer(serializers.ModelSerializer):
    """
    热搜词
    """

    class Meta:
        model = HotSearchWords
        fields = ('__all__')


class BannerSerializer(serializers.ModelSerializer):
    """"
    轮播图
    """

    class Meta:
        model = Banner
        fields = "__all__"


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    """"
    轮播图
    """

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)

    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        good_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return good_serializer.data

    """"
    首页分类
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"
