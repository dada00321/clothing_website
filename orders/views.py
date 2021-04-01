from django.urls import reverse # 對應到付費流程
from django.shortcuts import render
from django.shortcuts import redirect # 訂單送出後，重新導向至付費流程
from django.shortcuts import get_object_or_404 # 自訂管理後台
from django.contrib.admin.views.decorators import staff_member_required # 自訂管理後台

# 產生 PDF 電子收據
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import Order # 自訂管理後台
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created # 引入送出訂單後發送 email 的異步任務

""" 生成訂單(Order) """
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        # 若用 POST 送出"結帳"表單
        # 產生一個結帳表單:form，利用此表單建立 Order 實例
        # 並迭代購物車所有項目，使之成為 OrderItem 實例(與 Order 實例 相依)
        # 最後，(1)用這個 Order 實例 填充模板 (2)清空購物車
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            '''order = form.save() # 不考慮折扣'''
            # 儲存訂單 (考慮折扣)
            order = form.save(commit=False)
            if cart.coupon is not None:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item["product"],
                                         price=item["price"],
                                         quantity=item["quantity"])
            cart.clear()

            # 啟動異步任務 order_created()，寄信給 user
            order_id = order.id
            order_created.delay(order_id)

            '''
            # [Warning] (已結帳) 是連到 'created.html'
            return render(request,
                          "orders/order/created.html",
                          {"order": order})
            '''
            # 設定該 order 的 session
            request.session["order_id"] = order_id
            # 重新導向至付費流程
            return redirect(reverse("payment:process"))
    elif request.method == "GET":
        # 若用 GET 訪問，產生一個空表單
        # 用購物車&表單填充模板
        form = OrderCreateForm()
    # [Warning] (未結帳) 是連到 'create.html'
    return render(request,
                  "orders/order/create.html",
                  {"cart": cart, "form": form})

""" 自訂管理後台 """
# 由一組指定的訂單編號，取出訂單物件，透過自訂模板顯示在管理後台
# P.S. 以自訂模板"擴充"管理後台的 orders/order 細節資訊
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,\
                  "admin/orders/order/detail.html",
                  {"order": order})

""" 顯示 PDF 收據
       針對某筆訂單，產生 PDF 收據
"""
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html",
                            {"order": order})
    response = HttpResponse(content_type="application/pdf")

    pdf_file_name = f"order_{order_id}.pdf"
    response["Content-Disposition"] = f"filename={pdf_file_name}"

    stylesheet = weasyprint.CSS(settings.STATIC_ROOT +\
                                "css/pdf.css")
    weasyprint.HTML(string=html).write_pdf(response,
                            stylesheets=[stylesheet])
    return response
