from django.db import models
from django.core.validators import MinValueValidator,\
                                   MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from shop.models import Product
from coupons.models import Coupon

class Order(models.Model):
    first_name = models.CharField(_("first_name"),
                                  max_length=50)
    last_name = models.CharField(_("last_name"),
                                 max_length=50)
    email = models.EmailField(_("email"))
    address = models.CharField(_("address"),
                               max_length=250)
    zip_code = models.CharField(_("zip_code"),
                                max_length=20)
    #city = models.CharField(_("city"),
    #                        max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name="orders",
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),\
                                               MaxValueValidator(100)])
    class Meta:
        ordering=("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        # 透過 "items" 由 Order 反查: 某筆訂單對應的
        # 所有 OrderItem | 在支付流程會用到
        total_cost = sum(item.get_cost() for item in self.items.all())
        #result =  int(total_cost * (1-(self.discount / Decimal("100"))))
        result = int(total_cost - total_cost * (self.discount / Decimal(100)))
        '''
        return total_cost - total_cost * \
            (self.discount / Decimal(100))
        '''
        return result

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="items",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name="order_items",
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
