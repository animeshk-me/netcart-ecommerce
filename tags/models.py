from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from products.utils import unique_slug_generator

# the story of RDBMS starts 'Foreign keys!' yay!!!
from products.models import Product

class Tag(models.Model):
    title     = models.CharField(max_length = 120)
    slug      = models.SlugField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active    = models.BooleanField(default=True)
    products  = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
# here product_pre_save_receiver() itself acts as a receiver
# Tag class is the sender, after slugifying things they're gonna get saved