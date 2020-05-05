from rest_framework.pagination import (
    PageNumberPagination,
    # LimitOffsetPagination
)


# class PostLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 10
#     max_limit = 10

class PostPageNumberPagination(PageNumberPagination):
    page_size = 10

class ListPageNumberPagination(PageNumberPagination):
    page_size = 30

class MyHandycraftsPageNumberPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 200
