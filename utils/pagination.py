from rest_framework.pagination import LimitOffsetPagination

class ItemTotalPagination(LimitOffsetPagination):
    offset_query_param = 'item'
    limit_query_param = 'total'
    max_limit = 999999
    default_limit = 10