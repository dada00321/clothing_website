from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # (結帳後) 生成訂單
    path("create/", views.order_create, name="order_create"),

    # 自訂管理後台
    path("admin/orders/<int:order_id>/",\
         views.admin_order_detail,\
         name="admin_order_detail"),

    # PDF 收據
    path("admin/orders/<int:order_id>/pdf",\
         views.admin_order_pdf,\
         name="admin_order_pdf"),
]
