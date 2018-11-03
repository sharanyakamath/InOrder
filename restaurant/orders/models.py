from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import django.utils.timezone
# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'manager'),
      (2, 'customer'),
      (3, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    man_id = models.IntegerField(primary_key=True,default=1)
    

class Restaurant(models.Model):
	rest_id = models.IntegerField(primary_key=True, default=1007)
	name = models.CharField(max_length = 255)
	address = models.TextField()
	city = models.CharField(max_length = 255)
	state = models.CharField(max_length = 255)
	country = models.CharField(max_length = 255)
	man_id = models.ForeignKey(Manager,on_delete = models.CASCADE, default=1)
	image = models.ImageField(upload_to='restaurant',default=None)

class Customer(models.Model):
	cust_id = models.IntegerField(primary_key=True, default=123)
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)
    
class Item(models.Model):
	item_id = models.IntegerField(primary_key=True, default=1)
	name = models.CharField(max_length = 255)
	cost = models.IntegerField(default=0)
	description = models.TextField()
	image = models.ImageField(upload_to='item')
	rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=1007)

class Bill(models.Model):
	bill_id = models.IntegerField(primary_key=True, default=2)
	cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=123)
	rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=1007)
	total = models.IntegerField(default=0)

class Order(models.Model):
	bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE, default=2)
	item_id = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)
	quantity = models.IntegerField(default=0)