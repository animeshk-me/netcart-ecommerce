from django.shortcuts import render
from products.models import Product
from django.db.models import Q

def search_product_list_view(request):   # a function-based-view
    query = request.GET.get('q')   # ['q']
    print(request.GET) #request.GET is a python dictionary
    if query is not None:
        # queryset = Product.objects.filter(title__icontains=query) this our old bad queryset
        lookup = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(tag__title__icontains=query)#it is much like saying product_obj.tag_set.filter(title__icontains='black')
         ) 
        queryset = Product.objects.filter(lookup).distinct()
    else:
        queryset = Product.objects.none()    
    context = {
        'Object_list' : queryset
    }
    return render(request, 'search/search_view.html', context)


# ____________________IMPORTANT POINTS___________________

# 1.  request.GET is a python dictionary, literally a
#     method_dictionary e.g. <QueryDict: {'q': ['shirt']}> . So yes, to
#     access the 'value' element i.e. 'shirt' from the key-value pair
#     available in this mehtod_dictionary we could simply do request.GET
#     ['q'] but if that product list won't have anything in it and it 
#     returns 'None' then that method gives error 'MultiValueDictKeyError 
#     at /search/'. Therefore we use '.get()' to extract the value 
#     associated with the conventional(also default) key 'q'.

# 2.  "queryset = Product.objects.filter(title__icontains=query)" this finds
    # the value of key 'q' only in the 'title'. But, if we want it to be
    # searched in other attributes of a product as well, we take help of 'Q'
    # this method allows us to search a cetain value in multiple attributes.

# 3.   '.distinct()' allows us to not show multiple cards based on the query 
# matching in the multiple attributes.
