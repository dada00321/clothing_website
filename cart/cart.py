from decimal import Decimal
from django.conf import settings
from coupons.models import Coupon
from shop.models import Product
from math import ceil

class Cart(object):
    """ 初始化購物車 """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = dict()
        self.cart = cart
        # 初始化優惠券ID => 從 session 取值
        self.coupon_id = self.session.get("coupon_id")

    """ 新增商品至購物車 或 調整訂購數量 """
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart.setdefault(product_id,
                                 {"quantity": 0,
                                  "price": str(product.price)})
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    """ 設定 session 的 modified 屬性，確保已儲存當前狀態 """
    def save(self):
        self.session.modified = True

    """ 從購物車中移除商品 """
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()

    """ 將傳入整數轉為具有千分號的字串並回傳 """
    def get_num_with_separators(self, n):
        n = str(n)
        prefix = n[:len(n)-3*(len(n)//3)]
        suffix = n[len(n)-3*(len(n)//3):]
        result = prefix + (',' if len(prefix)>0 and len(suffix)>0 else '')
        result += ','.join([suffix[3*i:3*(i+1)] for i in range(len(n)//3)])
        return result

    """ 取出所有購物車商品的 generator """
    def __iter__(self):
        selected_prod_ids = self.cart.keys()
        selected_prods = Product.objects.filter(id__in=selected_prod_ids)
        cart = self.cart.copy()
        for product in selected_prods:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["price_str"] = self.get_num_with_separators(Decimal(item["price"]))
            item["total_price_str"] = self.get_num_with_separators(item["price"] * item["quantity"])
            yield item

    """ 取得購物車中所有商品預訂總數量(非商品個數) """
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    """ 取得購物車中所有商品預訂總金額(原價) """
    def get_total_price(self, type_="str"):
        result = sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
        if type_ == "val":
            return result
        elif type_ == "str":
            return self.get_num_with_separators(result)

    """ 清空購物車 session """
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    """ 若購物車 session 中存在 coupon_id 屬性
        則回傳該 coupon_id 相應的 coupon  """
    @property
    def coupon(self):
        if self.coupon_id is not None:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    """ 若購物車包含一張優惠券，則計算出折扣百分比 (?% Off)
        並回傳「折抵金額」 (若無折扣，則回傳 0)
        e.g., coupon.discount(0~100) => 15
              discount_percentage(discount/100) => 0.15
              return_value => 原價 * 0.15  """
    def get_discount_amount(self, type_="str"):
        if self.coupon is not None:
            discount_percentage =  self.coupon.discount / Decimal("100")
            result = int(ceil(discount_percentage * self.get_total_price(type_="val")))
            if type_ == "val":
                return result
            elif type_ == "str":
                return self.get_num_with_separators(result)
        else:
            return Decimal("0")

    """ 回傳「折扣後總金額」 (若無則回傳原價) """
    def get_total_price_after_discount(self, type_="str"):
        result = self.get_total_price(type_="val") - Decimal(self.get_discount_amount(type_="val"))
        if type_ == "val":
            return result
        elif type_ == "str":
            return self.get_num_with_separators(result)

    """ 回傳數值型態的「折扣後總金額」
        (給模板使用，因為 Django 模板不接收參數) """
    def get_total_price_after_discount_val(self):
        return self.get_total_price_after_discount("val")
