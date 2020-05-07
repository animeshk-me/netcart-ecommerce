from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save  #we want to slugify before saving 
from .utils import unique_slug_generator  #this is being done because I want to generate a unique a unique slug for every Product object.


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True) #just to not write '.filter()' in the
        # return statement of the overridden all(), we define this custom
        # queryset.


# (.objects) used in the python shell to retrieve data using (.get) and 
# create data using (.create), is just a default Model-manager. So, in order 
# to make our custom ModelManager we have to create it inside .models.

class ProductManager(models.Manager): #our custom Model-manager

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


    def all(self):  # lets override all function.
        return self.get_queryset().active()     # look at the featured(), 
        # how we did that is another way of doing the same thing, but there 
        # we are not required to define a custom queryset. Here we gotta
        # define a custome queryset called 'active()'.

    def featured(self): #return those tuples which have featured = True
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, my_id):
        qs = self.get_queryset().filter(id=my_id) #returns a full queryset
        if qs.exists() and qs.count() == 1:
            return qs.first() #first element of the queryset(though only one is there)
        else:
            return None
    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug) #returns a full queryset
        if qs.exists() and qs.count() == 1:
            return qs.first() #first element of the queryset(though only one is there)
        else:
            return None

# self.get_queryset() takes the place of Product.objects, so this returns that instance which has id = my_id.


#___________OUR Usual Product Model___________________
class Product(models.Model):
    title       = models.CharField(max_length = 100)
    slug        = models.SlugField(blank=True)
    description = models.TextField(default='No description is available.')
    price       = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=False)
    image       = models.ImageField(upload_to='products/', null=True, blank=True) #these files get uploaded to ecommerce/static_cdn/media_root
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    #simply record the time when its gonna get saved our database.

    objects     = ProductManager()
# above 'ProductManager' is not overwriting the defaults it is just extending
# to it, I mean you can still use .get() and .all() but you are able to use 
# '.get_by_id()' also.

    def __str__(self):    #this is just for representation on the Dashboard.
        return self.title  #so that the Dashboard writes 'T-Shirt' instead of
                             #'Product object'.

    def get_absolute_url(self):
        return reverse('products_url:product_detail_slug', kwargs={'slug' : self.slug})

   
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
# here product_pre_save_receiver() itself acts as a receiver
#Product class is the sender, after slugifying things they're gonna get saved.



