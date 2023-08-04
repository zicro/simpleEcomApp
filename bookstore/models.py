from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=140, null=True)
    email = models.EmailField(max_length=140, null=True)
    phone = models.CharField(max_length=15, null=True)
    age = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    CATEGORY = (
        ('Horror', 'Horror'),
        ('Fantasy', 'Fantasy'),
        ('Classic', 'Classic'),
        ('Comics', 'Comics'),
    )
    name = models.CharField(max_length=140, null=True)
    author = models.CharField(max_length=140, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=120, null=True, choices=CATEGORY)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Cancelled'),
        ('Delivered', 'Delivered'),
        ('in progress', 'in progress'),
        ('Out of Order', 'Out of Order'),
        ('Cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60,null=True, choices=STATUS)

    def __str__(self):
        return self.status