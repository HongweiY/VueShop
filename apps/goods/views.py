from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .filters import GoodsFilter
from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Create your views here.
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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


class CategoryListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
