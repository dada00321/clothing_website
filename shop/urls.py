from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    # [商品列表頁] 無參數: 全部商品
    path("", views.product_list, name="product_list"),

    # [商品列表頁] category_slug 參數: 指定目錄下的所有商品
    path("<slug:category_slug>/", views.product_list,
         name="product_list_by_category"),

    # [商品詳情頁] id, slug 參數: 具有某 id, slug 的特定商品
    path("<int:id>/<slug:product_slug>/",
         views.product_detail,
         name="product_detail"),
]
