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

    # class Meta:
    # 	permissions = (
    # 		("can_add_restaurant", "Can add restaurant"),
    # 		)
    # def has_perm(self, perm, obj=None):
    # 	return self.can_add_restaurant

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    man_id = models.IntegerField(primary_key=True,default=1)
    PERMISSION_CHOICES = (
      (1, 'add'),
      (2, 'add_edit'),
      (3, 'add_edit_delete'),
    )
    permissions = models.PositiveSmallIntegerField(choices=PERMISSION_CHOICES, default=1)
    

class Restaurant(models.Model):
	rest_id = models.IntegerField(primary_key=True, default=1007)
	name = models.CharField(max_length = 255)
	address = models.TextField()
	city = models.CharField(max_length = 255)
	state = models.CharField(max_length = 255)
	country = models.CharField(max_length = 255)
	man_id = models.ForeignKey(Manager,on_delete = models.CASCADE, default=1)
	image = models.ImageField(upload_to='restaurant',default=None)
	# class Meta:
	# 	permissions = (("can_add_restaurant", "Can add restaurant"),)

class Customer(models.Model):
	cust_id = models.IntegerField(primary_key=True, default=123)
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)
	PERMISSION_CHOICES = (
      (1, 'regular'),
      (2, 'premium'),
      (3, 'gold'),
    )
	permissions = models.PositiveSmallIntegerField(choices=PERMISSION_CHOICES, default=1)
    
class Item(models.Model):
	item_id = models.IntegerField(primary_key=True, default=1)
	name = models.CharField(max_length = 255)
	cost = models.IntegerField(default=0)
	description = models.TextField()
	image = models.ImageField(upload_to = 'media/item')
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

class Feedback(models.Model):
	feed_back = models.CharField(max_length = 255)
	cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE, default=123)
	rest_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE, default=1007)

# class Permission(models.Model):
# 	userid = models.IntegerField(primary_key=True, default=1007)
# 	can_add_restaurant = models.IntegerField(default=0)