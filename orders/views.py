import time
import stripe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from carts.models import Cart
from .models import Order

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except:
    stripe_pub = "pk_test_Lc1VPKGWfVIvUMaBEgdNuNHM00Dsa8akHY"
    stripe_secret = "sk_test_plkTsRU0LvReg1DmHlcR6hZJ00WUC7dZhb"

stripe.api_key = stripe_secret

def orders(request):
    context = {}
    template = "orders/user.html"
    return render(request, template, context)

@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("cart_app:cart", kwargs={}))
    
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order(cart=cart)
        new_order.cart = cart
        new_order.user = request.user
        new_order.save()
    except:
        new_order = None
        return HttpResponseRedirect(reverse("cart_app:cart", kwargs={}))
    final_amount = 0
    if new_order is not None:
        new_order.total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()
    try:
        address_added =request.GET.get("address_added")
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None
    current_address = UserAddress.objects.filter(user=request.user)
    billing_address = UserAddress.objects.get_billing_address(user=request.user)

    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None
            pass
        if customer is not None:
            try:
                billing_a = request.POST['billing_address']
                shipping_a = request.POST['shipping_address']
            except:
                return HttpResponseRedirect(reverse("orders:checkout", kwargs={}))
            try:
                billing_address_instance = UserAddress.objects.get(id=billing_a)
            except:
                billing_address_instance = None
            try:
                shipping_address_instance = UserAddress.objects.get(id=shipping_a)
            except:
                shipping_address_instance = None
            token = request.POST['stripeToken']
            # card = stripe.Customer.create_source(
            #         user_stripe,
            #         source=token,
            #         )
            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="inr",
                source=token,
                description="Charge for %s" %(request.user.username),
                )
            # print(charge)
            if charge["captured"]:
                new_order.status = "paid"
                new_order.shipping_address = shipping_address_instance or None
                new_order.billing_address = billing_address_instance or None
                new_order.save()
                del request.session['cart_id']
                messages.success(request, "Thank you for your order!")
                return HttpResponseRedirect(reverse("orders:user-orders", kwargs={}))
        
    context = {
        "order": new_order,
        "final_amount": final_amount,
        "current_address": current_address,
        "address_form": address_form,
        "billing_address": billing_address,
        "stripe_pub": stripe_pub,
        }
    template = "orders/checkout.html"
    return render(request, template, context)
