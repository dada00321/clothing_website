import braintree
from django.shortcuts import render, redirect,\
                             get_object_or_404
from orders.models import Order
from .tasks import send_invoice # 引入交易成功後發送 email 的異步任務
'''
# 將 PDF 電子收據 作為 email 附件送到支付訂單的用戶信箱
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO
'''

def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == "GET":
        # 若發送 GET 請求，產生 client token 作為後續使用
        # 並用 order, client_token 填充模板，導向至交易進行頁
        client_token = braintree.ClientToken.generate()
        return render(request, "payment/process.html",\
                      {"order": order,\
                       "client_token": client_token })

    elif request.method == "POST":
        # 若發送 POST 請求，代表用戶已填寫完支付資訊並送出表單
        # 取得 nonce，並向 Braintree 驗證
        # 依成功與否，重新導向到交易成功/交易取消頁

        # 取得 nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # 建立並提交一筆 transaction
        result = braintree.Transaction.sale(
                    { "amount": str(int(total_cost)),
                      "payment_method_nonce": nonce,
                      "options": {"submit_for_settlement": True}
                    }
                 )

        if result.is_success:
            # 若交易成功:
            # (1) 將 order 的 is_paid 狀態設為 True
            order.is_paid = True
            order.braintree_id = result.transaction.id
            order.save()
            ##########################
            # (2) 並產生一份電子 PDF 收據，送信到該用戶 email
            '''
            subject = "【Cloth2U】 Your invoice"
            message = "Please kindly find the attached file," +\
                      " the invoice for your recent purchase."
            email_msg = EmailMessage(subject, message,
                                     settings.EMAIL_HOST_USER,
                                     [order.email])
            # 產生 PDF
            pdf_file_name = f"order_{order_id}.pdf"
            content_type = "application/pdf"
            html = render_to_string("orders/order/pdf.html",\
                                    {"order": order}).encode("utf-8")
            outstream = BytesIO()
            stylesheet = weasyprint.CSS(settings.STATIC_ROOT +\
                                "css/pdf.css")
            weasyprint.HTML(string=html).write_pdf(outstream,
                            stylesheets=[stylesheet])
            # 將渲染好的 html PDF 文件添加為 email 附件
            email_msg.attach(pdf_file_name,
                             outstream.getvalue(),
                             content_type)
            # 發送 email
            email_msg.send()
            '''
            # 啟動異步任務 send_invoice()，寄信給 user
            send_invoice.delay(order_id)
            ##########################
            # 跳轉至交易成功頁
            return redirect("payment:done")
        else:
            # 跳轉至交易取消頁
            return redirect("payment:canceled")

def payment_done(request):
    # 渲染模板並回傳: 交易成功頁
    return render(request, "payment/done.html")

def payment_canceled(request):
    # 渲染模板並回傳: 交易取消頁
    return render(request, "payment/canceled.html")
