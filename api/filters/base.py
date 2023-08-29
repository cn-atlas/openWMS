import django_filters
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser


class BaseFilter(django_filters.FilterSet):
    '''
    指定字段匹配搜索, 默认是精确匹配并支持 manufacturer__name 外键搜索
    但它将Django的双下划线约定作为API的一部分暴露出来。如果你想显式地命名过滤器参数，你可以显式地将它包含在FilterSet类中
    class ProductFilter(django_filters.rest_framework.FilterSet):
        manufacturer = django_filters.CharFilter(name="manufacturer__name")

    也可以通过重写类中字段来支持大于小于等条件搜索
    class ProductFilter(django_filters.rest_framework.FilterSet):
        min_price = django_filters.NumberFilter("price", lookup_expr='gte')
        max_price = django_filters.NumberFilter("price", lookup_expr='lte')

    请求可以这么写 http://example.com/api/products?category=clothing&max_price=10.00
    '''

    # title = django_filters.NumberFilter('age', lookup_expr='eq')
    # start = django_filters.DateFilter("send_date", lookup_expr='gte')
    # end = django_filters.DateFilter("send_date", lookup_expr='lte')

    class Meta:
        # pass
        model = None
        fields = {}
        # model = Channel
        # 精确过滤字段
        # fields = ['id']
        # fields = '__all__'


class AuditlogFilterMixin(object):
    '''
    Auditlog 过滤器
    '''

    @property
    def qs(self):
        qs = super().qs
        request_user = getattr(self.request, 'user', None)
        if isinstance(request_user, AnonymousUser):
            return []
        if request_user.is_superuser:
            return qs
        return qs.filter(actor=request_user)


class FilterMixin(object):
    '''
    基础过滤器，创建人、编辑人、或者管理员
    '''

    @property
    def qs(self):
        qs = super().qs
        request_user = getattr(self.request, 'user', None)
        if isinstance(request_user, AnonymousUser):
            return []
        if request_user.is_superuser:
            return qs
        return qs.filter(Q(creator=request_user) | Q(editor=request_user))
