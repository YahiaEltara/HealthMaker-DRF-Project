from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 2  # Number of items per page
    page_size_query_param = 'page_size'  # Allow the client to control the page size
    max_page_size = 100 


def get_user_related_field(relation_name):
    """
    Helper function to return the username field for related models.
    """
    return f"{relation_name}__user__username"