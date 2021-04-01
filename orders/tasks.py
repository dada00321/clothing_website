from celery import task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@task
def order_created(order_id):
    """
    當訂單建立時，發送 email 的任務
    P.S. 為「通知訂單成立的文字 email 訊息」，非 PDF收據
    """
    # 發信人: 官方email 收信人: 訂單所屬用戶email
    order = Order.objects.get(id=order_id)
    order_id = str(int(order_id)).zfill(8)
    subject = "【Cloth2U】 Order confirm"
    message = f"Dear {order.first_name} {order.last_name},\n\n"
    message += "You have successfully placed an order.\n"
    message += f"Your order id is  {order_id}"

    official_mail = settings.EMAIL_HOST_USER
    mail_sent = send_mail(subject, message,\
                          official_mail, [order.email])
    return mail_sent
