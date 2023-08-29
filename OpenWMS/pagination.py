from rest_framework.pagination import PageNumberPagination


class NoLimitNumPagination(PageNumberPagination):
    """
    设置无限制每页显示条目数量的分页器
    """
    page_size = 99999


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
