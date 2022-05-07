from djoser.views import UserViewSet
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
