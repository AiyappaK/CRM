from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer(models.Model):
    """docstring for customer."""
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200 , null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True )
    profile_pic = models.ImageField(default="b9lvanhagtwgayzit46n.jpeg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """docstring for tags."""
    name = models.CharField(max_length=200 , null=True)

    def __str__(self):
        return self.name

class products(models.Model):
    """docstring for products."""
    CATEGORY = (
                ('Indoor', 'Indoor'),
                ('Out door', 'Out Door'),

    )

    name = models.CharField(max_length=200 , null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200 , null=True, choices = CATEGORY)
    description = models.CharField(max_length=200 , null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class order(models.Model):
    """docstring for order."""
    STATUS = (
                ('Pending', 'Pending'),
                ('out for delivery', 'out for delivery'),
                ('deliverd', 'deliverd'),
    )
    customer = models.ForeignKey(customer, null=True, on_delete = models.SET_NULL)
    products = models.ForeignKey(products, null=True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200 , null=True, choices = STATUS)
    note = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.products.name
