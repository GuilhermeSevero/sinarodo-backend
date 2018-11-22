from rest_framework.pagination import LimitOffsetPagination, _positive_int
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'per_page'
    limit_query_description = 'Limite por página'
    offset_query_param = 'page'
    offset_query_description = 'Página a ser mostrada'

    def get_offset(self, request):
        try:
            return _positive_int(
                ((int(request.query_params[self.offset_query_param]) - 1) * int(
                    request.query_params[self.limit_query_param])),
            )
        except (KeyError, ValueError):
            return 0

    def get_paginated_response(self, data):
        return Response(
            data=data,
            headers={
                'x-total': self.count,
                'x-page': int(int(self.offset) / int(self.limit)) + 1 if self.offset > 0 else 1,
                'x-per-page': self.limit
            }
        )
