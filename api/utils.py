from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import BaseUserManager


class CustomPagination(PageNumberPagination):
    page_size = 2  # Number of items per page
    page_size_query_param = 'page_size'  # Allow the client to control the page size
    max_page_size = 100 



def get_user_related_field(relation_name):
    """
    Helper function to return the username field for related models.
    """
    return f"{relation_name}__user__username"


# class ApiUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         """
#         Create and return a regular user with a username, password, and other fields.
#         """
#         if not username:
#             raise ValueError('The Username must be set')
#         # Ensure age and gender are required for regular users
#         if 'age' not in extra_fields or 'gender' not in extra_fields or 'role' not in extra_fields:
#             raise ValueError('Age, gender and role are required for regular users')
        
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         """
#         Create and return a superuser with a username, password, and other fields.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         # For superuser, do not enforce 'age' and 'gender' fields
#         extra_fields.setdefault('age', 10)  # Or any default value
#         extra_fields.setdefault('gender', 'male')  # Or any default value
#         extra_fields.setdefault('role', 'Admin')  # Or any default value

#         return self.create_user(username, password, **extra_fields)