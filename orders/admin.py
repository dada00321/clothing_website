''' Orders 管理後台 '''
from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime
import pytz
from .models import Order, OrderItem
# 擴展管理後台
from django.urls import reverse
from django.utils.safestring import mark_safe

''' order_detail: 用於「擴展管理後台」(orders/admin.py)
admin => urls => views => template
(1) 由 namespace_name 對應到 ./urls.py 的特定 path (name參數)
再由此 path 送交到 view: admin_order_detail (=> 再填充模板)
(2) view: admin_order_detail 需傳入 order_id 參數 (以找出特定 Order obj)
故此處 (admin.py) 需以 args=[obj.id] 將管理後台選中 '訂單ID'
用 reverse() 一併對應到 ./urls.py 的特定 path
P.S. mark_safe(): 避免 XSS Attack
'''
def order_detail(obj):
    namespace_name = "orders:admin_order_detail"
    link = reverse(namespace_name, args=[obj.id])
    return mark_safe(f'<a href="{link}">View</a>')

def order_pdf(obj):
    namespace_name = "orders:admin_order_pdf"
    link = reverse(namespace_name, args=[obj.id])
    return mark_safe(f'<a href="{link}">PDF</a>')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "is_paid",
                    order_detail, order_pdf,
                    "first_name", "last_name",
                    "email", "address", "zip_code",
                    "created", "updated"] # "city",
    list_filter = ["is_paid", "created", "updated"]
    inlines = [OrderItemInline]

    '''
    def utc_to_local(utc_dt, local_tz="Asia/Taipei"):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt) # .normalize might be unnecessary

    def aslocaltimestr(utc_dt):
        return utc_to_local(utc_dt)
    '''
    def export_to_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment;"\
             f"filename={opts.verbose_name}.csv"
        writer = csv.writer(response)

        fields = [field for field in opts.get_fields()\
                  if not field.many_to_many\
                  and not field.one_to_many]

        # 寫入標題列(第一列)
        # P.S. Excel 開啟 CSV 檔案時，如果第一個表格單元
        # 是'ID'，會判斷為 SYLK 檔案。'ID' 轉小寫就可正常開啟
        writer.writerow([field.verbose_name\
                         if "ID" not in field.verbose_name\
                         else "id"\
                         for field in fields])

        # 寫入各資料列
        # P.S. 若不設定時區，datetime 會自動轉成格林威治時間
        # 故用以下方式保留 (1)原始時間數值 (2)時區資訊
        TPE_tz = pytz.timezone("Asia/Taipei")
        for obj in queryset:
            data_row=[]
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.astimezone(TPE_tz)\
                                 .strftime("%Y-%m-%d %H:%M:%S %z")
                data_row.append(value)
            writer.writerow(data_row)
        return response

    export_to_csv.short_description = "輸出為CSV檔案"
    actions = [export_to_csv]
