from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from decimal import Decimal
from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):


    def create_new_cart(self, user=None):
        user_obj = user
        cart_object = self.model.objects.create(user=user_obj)
        return cart_object

    # def get_or_create(self, request):
    #     Cart_obj_id = request.session.get('cart_id', None)
    #     qs = self.get_queryset().filter(id=Cart_obj_id) 
    #     if qs.count() == 1: 
    #         Cart_obj = qs.first()  
    #         if Cart_obj.user is None: 
    #             Cart_obj.user = request.user 
    #             Cart_obj.save()          
    #     else: # No 'Cart' object exists in this session. So create it.
    #         Cart_obj = Cart.objects.create(user=request.user)
    #         request.session['cart_id'] = Cart_obj.id # Now make the new Cart_obj's id as the value to the key 'cart_id'
    #     return Cart_obj

    def get_or_create(self, request):
        Cart_obj_id = request.session.get('cart_id', None)
        print('id')
        print(Cart_obj_id)
        qs = self.get_queryset().filter(id=Cart_obj_id) 
        print('qs')
        print(qs)
        # if qs.count() == 1: 
        try: 
            user_cart_obj = Cart.objects.get(user=request.user)
            Cart_obj = user_cart_obj
            print('11')
            print(Cart_obj)
            request.session['cart_id'] = Cart_obj.id
        except Cart.DoesNotExist:
            Cart_obj = Cart.objects.create(user=request.user)
            print('12')
            print(Cart_obj)
            request.session['cart_id'] = Cart_obj.id # Now make the new Cart_obj's id as the value to the key 'cart_id'
        # else: # No 'Cart' object exists in this session. So create it.
        #     Cart_obj = Cart.objects.create(user=request.user)
        #     print('2')
        #     print(Cart_obj)
        #     request.session['cart_id'] = Cart_obj.id # Now make the new Cart_obj's id as the value to the key 'cart_id'
        return Cart_obj


    # ________________  BELOW THINGS WERE BY JUSTIN MITCHEL_________________ 
    # def new_or_get(self, request):
    #     Cart_obj_id = request.session.get('cart_id', None)
    #     qs = self.get_queryset().filter(id=Cart_obj_id)
    #     if qs.count() == 1:
    #         new_obj = False
    #         Cart_object = qs.first()
    #         if request.user.is_authenticated and Cart_object.user is None:
    #             Cart_object.user = request.user
    #             Cart_object.save()
    #     else:
    #         Cart_object = Cart.objects.new(user=request.user)
    #         new_obj = True
    #         request.session['cart_id'] = Cart_object.id
    #     return Cart_object, new_obj 


    # def new(self, user=None):
    #     user_object = None
    #     if user is not None:
    #         if user.is_authenticated:
    #             user_object = user
    #     return self.model.objects.create(user=user_object)

class Cart(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products  = models.ManyToManyField(Product, blank=True)
    total     = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects   = CartManager()

    def __str__(self):
        return str(self.id)




def cart_m2m_changed_receiver(sender, instance, action, *args, **kwargs):
    if( action=='post_add' or action=='post_remove' or action=='post_clear'):
        products_in_cart = instance.products.all()
        total = 0
        for prod_obj in products_in_cart:
            total = total + prod_obj.price
        if instance.total != total:
            instance.total = total
            instance.save()

m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)
    

def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.total > 0:
        instance.total = Decimal(instance.total) + Decimal(10)
    else:
        instance.total = Decimal(0.00)

pre_save.connect(cart_pre_save_receiver, sender=Cart)
