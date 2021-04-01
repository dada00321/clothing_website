from django.forms import Form
from django.forms import TypedChoiceField, BooleanField,\
                         HiddenInput
from django.utils.translation import gettext_lazy as _

MAX_QUANTITY = 20
PRODUCT_QUANTITY_CHOICE = [(i, str(i)) for i in range(1, MAX_QUANTITY+1)]

class CartAddProductForm(Form):
    quantity = TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICE,
                                coerce=int,
                                label=_("Quantity"))
    update = BooleanField(required=False,
                          initial=False,
                          widget=HiddenInput)
