from django.http import HttpResponse
from rest_framework.views import APIView
from WMS.models.inventory import WmsInventoryHistory
from api.filters.WMSFilter import WmsInventoryHistoryFilter
from im_export.views.permissions import CanExport
from api.filters.object_range import get_qs_in_permission
from im_export.resources.WMS.inventory import WmsInventoryHistoryResource

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from im_export.views.base import field_to_openapi_type, get_export_file_name


# class ImportWmsInventoryHistoryView(APIView):
#     def post(self, request):
#         resource = WmsInventoryHistoryResource()
#         dataset = Dataset()
#         new_books = request.FILES['file']  # Assuming you are uploading a file
#
#         imported_data = dataset.load(new_books.read())
#         result = resource.import_data(dataset, dry_run=True)  # Dry run to check validity
#
#         if not result.has_errors():
#             resource.import_data(dataset, dry_run=False)  # Perform the actual import
#             return Response({'message': 'Import successful'})
#         else:
#             return Response({'message': 'Import failed', 'errors': result.errors})

class ExportWmsInventoryHistoryView(APIView):
    """
    按照对应数据接口的 filter 文档传参即可
    访问权限：can_view_model
    数据范围权限：对应接口一致
    """
    # 接口权限，自定义权限筛选器要求额外增加 Meta 字段，且 Meta.model 必填
    permission_classes = [CanExport]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name=param, in_=openapi.IN_QUERY, type=field_to_openapi_type(field),
                              description=field.label)
            for param, field in WmsInventoryHistoryFilter.base_filters.items()
        ]
    )
    def get(self, request):
        _resource = WmsInventoryHistoryResource()
        # Apply filters based on query parameters
        _query_params = dict(request.query_params)
        _file_name = get_export_file_name(self, request)
        if _query_params:
            queryset = WmsInventoryHistory.objects.filter(is_show=True)
            _filter = WmsInventoryHistoryFilter(request.query_params, queryset)
            # 必填，权限范围
            filtered_qs = get_qs_in_permission(_filter.qs, request.user)
            dataset = _resource.export(queryset=filtered_qs)
        else:
            dataset = _resource.export()

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(_file_name)
        return response

    class Meta:
        model = WmsInventoryHistory
