from django.shortcuts import redirect #,render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["couponid"] = None
    # 重導向到購物車頁面，已在購物車使用優惠券
    return redirect("cart:cart_detail")
