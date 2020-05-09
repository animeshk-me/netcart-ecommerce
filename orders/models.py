# from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from decimal import Decimal

from accounts.models import UserAddress
from carts.models import Cart
from products.utils import unique_order_id_generator

# USER = get_user_model()

# dropdown list for merchents
ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

try:
    tax_rate =settings.DEFAULT_TAX_RATE
except:
    tax_rate = 0.18

class Order(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    order_id        = models.CharField(max_length=120, blank=True, unique=True)
    # billing_profile = ?
    shipping_address= models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING, related_name='shipping_address', null=True)
    billing_address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING, related_name='billing_address', null=True)
    cart            = models.ForeignKey(Cart,on_delete=models.DO_NOTHING)
    status          = models.CharField(max_length=120, default= 'created', choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=40.00, max_digits=20, decimal_places=2)
    total           = models.DecimalField(default=00.00, max_digits=20, decimal_places=2)

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        two_places = Decimal(10) ** -2
        tax = Decimal(Decimal("%s" %(tax_rate)) * Decimal(self.total)).quantize(two_places)
        return Decimal(self.total) + Decimal(self.shipping_total) + Decimal(tax)

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)