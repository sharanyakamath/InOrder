from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Customer, Manager, Restaurant, Item, Order
import datetime
import pdfkit
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.

def customer_signup(request):
	if request.method == "POST":
		cust_id = request.POST['cust_id']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user = User(username=username, first_name=first_name, last_name=last_name, email=email, user_type=2)
		user.set_password(password)
		user.save()
		customer = Customer(cust_id=cust_id, user=user)
		customer.save()
		return redirect('customer_home', pk=customer.cust_id)
	else:
		return render(request, 'customer_signup.html')

def customer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.user_type == 2:
                    login(request, user)
                    return redirect('customer_home',pk=user.customer.cust_id) 
                else:
                    return render(request, 'customer_login.html', {'error_message': 'Invalid security staff credentials'})
            else:
                return render(request, 'customer_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'customer_login.html', {'error_message': 'Invalid login'})
    return render(request, 'customer_login.html')


def manager_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.user_type == 1:
                    login(request, user)
                    return redirect('manager_home', pk= user.manager.man_id) #, pk=user.security.id)
                else:
                    return render(request, 'manager_login.html', {'error_message': 'Invalid manager credentials'})
            else:
                return render(request, 'manager_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'manager_login.html', {'error_message': 'Invalid login'})
    return render(request, 'manager_login.html')    



def home(request):
	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')			


def manager_signup(request):
	if request.method == "POST":
		man_id = request.POST['man_id']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user = User(username=username, first_name=first_name, last_name=last_name, email=email, user_type=1)
		user.set_password(password)
		user.save()
		manager = Manager(man_id=man_id, user=user)
		manager.save()
		return redirect('manager_home', pk=manager.man_id)
	else:
		return render(request, 'manager_signup.html')

def manager_home(request,pk):
	manager = get_object_or_404(Manager, pk=pk)
	restaurants = Restaurant.objects.filter(man_id=pk)
	return render(request, 'manager_home.html', {'manager': manager, 'restaurants':restaurants})

def customer_home(request,pk):
	customer = get_object_or_404(Customer, pk=pk)
	restaurants = Restaurant.objects.all()
	return render(request, 'customer_home.html', {'customer': customer, 'restaurants': restaurants})


def register_restaurant(request,pk):
	if request.method == "POST":
		manager = Manager.objects.get(pk=pk)
		rest_id = request.POST['rest_id']
		name = request.POST['name']
		address = request.POST['address']
		city = request.POST['city']
		state = request.POST['state']
		country = request.POST['country']
		restaurant = Restaurant(rest_id=rest_id,name=name,address=address,city=city,state=state,country=country, man_id=manager)		
		restaurant.save()
		return redirect('reg_restaurant_home' , pk=restaurant.pk)
	else:
		return render(request, 'register_restaurant.html' , {'man_id' : request.user.manager.man_id })

def reg_restaurant_home(request,pk):
	restaurant = get_object_or_404(Restaurant, pk=pk)
	items = Item.objects.filter(rest_id=pk)
	return render(request, 'reg_restaurant_home.html', {'restaurant': restaurant, 'items':items})

def add_item(request,pk):
	if request.method == "POST":
		restaurant=Restaurant.objects.get(pk=pk)
		item_id = request.POST['item_id']
		name = request.POST['name']
		cost = request.POST['cost']
		description = request.POST['description']
		image = request.FILES['image']
		#print(image)
		#print(description)
		item = Item(item_id=item_id,name=name,cost=cost,image=image,description=description,rest_id=restaurant)
		item.save()
		return HttpResponseRedirect('/orders/add_item/' + str(pk))
	else:
		restaurant=Restaurant.objects.get(pk=pk)
		return render(request,'add_item.html',{'restaurant': restaurant})	



