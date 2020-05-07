from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404

from .models import Product
from carts.models import Cart

# Notice the differences between class and function based views.

class ProductListView(ListView):  # a class-based-view
    queryset = Product.objects.all()
    template_name = 'products/list.html'

    # Now, the problem is we do not what exactly is the context passed by
    # the class ProductListView, that's why we think function based views
    # are easy. To get the missing context of a class-based view we do the
    # following procedure.
    # This procedure is a builtin function for all class-based-views(CBV) 
    # and this can be called to get the context of that particle CBV.

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context 



def product_list_view(request):   # a function-based-view
    queryset = Product.objects.all()    
    context = {
        'Object_list' : queryset
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, my_id):
    # ___________METHOD: #1___________________
    # try:
    #     obj = Product.objects.get(id=my_id)
    # except Product.DoesNotExist:
    #     raise Http404    
    
    
    # ___________METHOD: #2___________________
    # qs = Product.objects.filter(id = my_id)
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()  #in this method only this line would have sufficed
    # else:
    #     raise Http404 

    # ___________METHOD: #3___________________ 
    obj = Product.objects.get_by_id(my_id) #custom manager function .get_by_id()
    if obj is None:  #checking if such id object is not found at all.
        raise Http404
    context = {
        'obj' : obj
    }
    return render(request, 'products/product_detail.html', context)


def product_detail_slug_view(request, slug):
    
    obj = Product.objects.get_by_slug(slug)# custom manager function .get_by_id()
    if obj is None:  #checking if such id object is not found at all.
        raise Http404
    if request.user.is_authenticated:
        Cart_object = Cart.objects.get_or_create(request)
        context = {
            'obj'     : obj,
            'cart_obj': Cart_object
        }
    else:
        context = {
            'obj'     : obj
        }
    return render(request, 'products/product_detail.html', context)

def featured_list_view(request): # using featured() makes it look very
    qs = Product.objects.featured()     # similar to the product_list_view
    context = {
        'Object_list' : qs
    }
    return render(request, 'products/featured_list.html', context)





     
