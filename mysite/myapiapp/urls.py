from django.urls import path

# from .views import hello_world_view
from .views import GroupsListView

app_name = 'myapiapp'

urlpatterns = [
    # path('hello/', hello_world_view, name="hello"),
    path('groups/', GroupsListView.as_view(), name="groups"),
]
