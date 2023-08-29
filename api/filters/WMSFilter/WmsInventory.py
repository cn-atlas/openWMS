import django_filters
from django.db.models import F
from WMS.models.inventory import WmsInventory
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsInventoryFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''
    quantity__gte = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity__lte = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')

    #  in_danger_quantity= django_filters.NumberFilter(method='danger_quantity')
    #
    # def danger_quantity(self, queryset, name, value):
    #     return queryset.filter(**{f'quantity__gte': F("item__abs_item__quantit")})

    class Meta:
        model = WmsInventory
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'rack__id': ['exact'], 'item__abs_item__number': ['exact'], 'item__abs_item__name': ['icontains'],
                  'item__id': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
