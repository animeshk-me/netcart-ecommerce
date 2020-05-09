import stripe
from django.conf import settings
from django.db import models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

stripe.api_key = settings.STRIPE_SECRET_KEY

class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    shipping = models.ForeignKey("UserAddress", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="user_address_shipping_default")
    billing = models.ForeignKey("UserAddress", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="user_address_billing_default")

    def __str__(self):
        return self.user.username

class UserAddressManager(models.Manager):
    def get_billing_address(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.get_address()
    
    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self.country, self.zipcode)
    
    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']

class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    stripe_id = models.CharField(max_length=120)

    def __str__(self):
        return self.stripe_id


def get_or_create_stripe(sender, user, *args, **kwargs):
    try:
        user.userstripe.stripe_id
    except UserStripe.DoesNotExist:
        customer = stripe.Customer.create(
        email = str(user.email)
        )
        new_user_stripe = UserStripe.objects.create(
            user = user,
            stripe_id = customer.id
            )


user_logged_in.connect(get_or_create_stripe)
