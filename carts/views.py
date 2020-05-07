from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from profiles.models import Profile
from django.http import HttpResponse


#______________________VERSION-1 OF MY ATTEMPTS__________________________

def cart_create(user=None):
    user_obj = None
    if user is not None and user.is_authenticated:
        user_obj = user
    cart_object = Cart.objects.create(user=user_obj)
    return cart_object


def cart_home(request):

    Cart_obj_id = request.session.get('cart_id', None)
    # if there is a value associated with the key 'cart_id', store that in a 
    # new variable called 'Cart_obj_id'. That is to check if there is a cart 
    # existing in current moment, if yes then it will not return "None"
    qs = Cart.objects.filter(id=Cart_obj_id) # Now get all the 'Cart' objects with id = Cart_obj_id
    if qs.count() == 1: # if there exists only one such "Cart" object.
        Cart_obj = qs.first() # then assign that object into 'Cart_obj'
        if request.user.is_authenticated: # if the user is logged in 
            if Cart_obj.user is None: # if the current 'Cart' was actually started by an anonymous user
                Cart_obj.user = request.user # then make that cart to the 'logged in' user.
                Cart_obj.save()
            # else: # Now we have to create a new 'Cart' object altogether.
            #     Cart_obj = Cart.objects.create(user=request.user)          
    else: # No 'Cart' object exists in this session. So create it.
        Cart_obj = cart_create(user=request.user)
        request.session['cart_id'] = Cart_obj.id # Now make the new Cart_obj's id as the value to the key 'cart_id'
                   

    # request.session['first'] = 'animesh' #(Setter)
    # print(request.session['first']) # bad practice
    # print(request.session.get('first', 'Unknown')) # (Getter) wow we 
    # have now created a session variable, literally 'first' is acting here 
    # like a session variable. Unknown can be set as a default if there is no 
    # key-value pair for the key 'first'


    return render(request, 'carts/home.html', {})




#___________________________IMPORTANT NOTE______________________________
# Above functions were created in such a way that even anonymous users can 
# make use of carts. Those functions are according to the video we have 
# watched. But we have decided here to allow only authenticated users to make 
# use of cart. Thus below functions are made by us.

#______________________VERSION-2 OF MY ATTEMPTS__________________________

# this version, expects the template tags' IF conditions to decide that 
# Anonymous users have to be redirected to cart_home_fail() and logged in 
# users to cart_home2().

def cart_create2(user=None):  # THIS WAS NOT NEEDED ACTUALLY, THAT'S WHY IN THE NEXT VERSION OF 'cart_home()' IT IS REMOVED.
    user_obj = user
    cart_object = Cart.objects.create(user=user_obj)
    return cart_object

def cart_home2(request):

    Cart_obj_id = request.session.get('cart_id', None)

    qs = Cart.objects.filter(id=Cart_obj_id) 
    if qs.count() == 1: 
        Cart_obj = qs.first()  
        if Cart_obj.user is None: 
            Cart_obj.user = request.user 
            Cart_obj.save()          
    else: # No 'Cart' object exists in this session. So create it.
        Cart_obj = cart_create2(user=request.user)
        request.session['cart_id'] = Cart_obj.id # Now make the new Cart_obj's id as the value to the key 'cart_id'

    return render(request, 'carts/home.html', {})

def cart_home_fail(request):  # TO BE USED IN BOTH VERSIONS- 2 AND 3
    return render(request, 'carts/home_fail.html', {})

#______________________VERSION-3 OF MY ATTEMPTS__________________________

# In this version all the logic is handled by ModelManager in .models.
# This version is inspired by Justin Mitchel
def cart_home3(request):
    if request.user.is_authenticated:
        Cart_obj = Cart.objects.get_or_create(request)
        context = { 'cart_obj' : Cart_obj }
        return render(request, 'carts/home.html', context)
    else: # Unauthorized anonymous users arn't allowed to use 'Cart' facility
        return render(request, 'carts/home_fail.html', {})


def add_to_cart(request):
    product_obj_id = request.POST.get('product_id')
    try:
        product_obj = Product.objects.get(id=product_obj_id)
    except Product.DoesNotExist:
        print('Product not found')
        return redirect('cart_app:cart')
    if request.user.is_authenticated:
        Cart_object = Cart.objects.get_or_create(request)
        Cart_object.products.add(product_obj)
        return redirect('cart_app:cart')
    else: # Unauthorized anonymous users arn't allowed to use 'Cart' facility
        return render(request, 'carts/home_fail.html', {})

def remove_from_cart(request):
    product_obj_id = request.POST.get('product_id')
    try:
        product_obj = Product.objects.get(id=product_obj_id)
    except Product.DoesNotExist:
        print('Product not found')
        return redirect('cart_app:cart')
    if request.user.is_authenticated:
        Cart_object = Cart.objects.get_or_create(request)
        Cart_object.products.remove(product_obj)
        # request.session['remove'] = True
        return redirect('cart_app:cart') 
    else: # Unauthorized anonymous users arn't allowed to use 'Cart' facility
        return render(request, 'carts/home_fail.html', {})
    
    


def checkout_view(request):
    Cart_object = Cart.objects.get_or_create(request) 
    try:
        profile_obj = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return HttpResponse('<html><h2>Profile Does Not Exist</h2></html>')
    context = { 
        'cart_obj' : Cart_object,
        'profile_object' : profile_obj
    }
    return render(request, 'carts/checkout.html', context)


#______________If above things don't work, this will work_____________________
# def cart_home_justin(request):        # made by Justin
#     Cart_object = Cart.objects.new_or_get(request)
#     return render(request, 'carts/home.html', {})