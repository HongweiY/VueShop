from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .filters import GoodsFilter
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, CategorySerializer, HotSearchWordsSerializer, BannerSerializer, \
    IndexCategorySerializer


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Create your views here.
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        商品列表页, 分页， 搜索， 过滤， 排序
        """
    # throttle_classes = (UserRateThrottle, )
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 配置权限链接
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # 记录用户点击数
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchWordsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    热搜词
    """
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class = HotSearchWordsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页分页
    """
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer
