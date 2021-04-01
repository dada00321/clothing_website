from celery import task
# 將 PDF 電子收據 作為 email 附件送到支付訂單的用戶信箱
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO
from orders.models import Order

@task
def send_invoice(order_id):
    """
    當交易成功時，發送 email 的任務
    P.S. 為「PDF 收據」，非 通知訂單成立的文字 email 訊息
    """
    order = Order.objects.get(id=order_id)
    subject = "【Cloth2U】 Your invoice"
    message = "Please kindly find the attached file," +\
              " the invoice for your recent purchase."
    email_message = EmailMessage(subject, message,
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
    email_message.attach(pdf_file_name,
                         outstream.getvalue(),
                         content_type)
    # 發送 email
    email_message.send()
