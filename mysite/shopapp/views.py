from timeit import default_timer

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.viewsets import ModelViewSet

from .forms import ProductForm, GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """

    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]

    filterset_fields = [
        "name",
        "description",
        "prices",
        "discount",
        "archived",
    ]

    ordering_fields = [
        "name",
        "prices",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ('laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999)
        ]

        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }

        return render(request, 'shopapp/group_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-detalis.html'
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"
    # queryset = Product.objects.filter(archived=False)


class ProductListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


# def create_product(request: HttpRequest) -> HttpResponse:
#
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             # Product.objects.create(name=name, price=price)
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {
#         "form": form
#     }
#
#     return render(request, "shopapp/create-product.html", context=context)

class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        return self.request.user.is_superuser

    model = Product
    fields = "name", "prices", "description", "discount", "preview"
    # form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "prices", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = Order.objects.select_related("user").prefetch_related("products")
