from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 1  # Number of items per page
    page_size_query_param = 'page_size'  # Allow the client to control the page size
    max_page_size = 100 