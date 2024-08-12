from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    OrderListView,
    ProductCreateView,
    ProductDetailsView,
    ProductListView,
    OrderDetailView,
    ProductUpdateView,
    ProductDeleteView,
    ProductViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name="product_details"),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name="product_update"),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details")
]