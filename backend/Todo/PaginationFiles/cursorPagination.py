from rest_framework.pagination import PageNumberPagination


class myPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 15