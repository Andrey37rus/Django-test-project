from django.contrib.auth.models import Group
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import GroupListSerializer


# @api_view()
# def hello_world_view(request: Request) -> Response:
#     return Response({"message": "Hello world!"})


# class GroupsListView(ListModelMixin, GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupListSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)


class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupListSerializer
