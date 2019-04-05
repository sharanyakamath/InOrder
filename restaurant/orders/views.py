from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Customer, Manager, Restaurant, Item, Order, Bill, Feedback
import datetime
import pdfkit
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# Create your views here.

# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType

# content_type = ContentType.objects.get_for_model(Restaurant)
# permission = Permission.objects.get(content_type=content_type, codename='can_add_restaurant')

def customer_signup(request):
	if request.method == "POST":
		cust_id = request.POST['cust_id']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		# permissions = request.POST['permissions']
		user = User(username=username, first_name=first_name, last_name=last_name, email=email)
		user.set_password(password)
		user.save()
		customer = Customer(cust_id=cust_id, user=user)
		customer.save()
		login(request, user)
		return redirect('customer_home', pk=customer.cust_id)
	else:
		return render(request, 'customer_signup.html')

def customer_login(request):
	if request.method == "POST":
		userid = request.POST['userid']
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				customer = get_object_or_404(Customer, pk=userid)
				if customer:
					login(request, user)
					return redirect('customer_home',pk=customer.cust_id) 
				else:
					return render(request, 'customer_login.html', {'error_message': 'Invalid security staff credentials'})
			else:
				return render(request, 'customer_login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'customer_login.html', {'error_message': 'Invalid login'})
	return render(request, 'customer_login.html')


def manager_login(request):
	if request.method == "POST":
		userid = request.POST['userid']
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				manager = get_object_or_404(Manager, pk=userid)
				if manager:
					login(request, user)
					return redirect('manager_home', pk= manager.man_id) #, pk=user.security.id)
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
		# permissions = request.POST['permissions']
		user = User(username=username, first_name=first_name, last_name=last_name, email=email)
		user.set_password(password)
		user.save()

		# content_type = ContentType.objects.get_for_model(Restaurant)
		# permission = Permission.objects.get(codename='add_restaurant', content_type=content_type,)
		# user.user_permissions.add(permission)
		# user.save()

		# manager = Manager(man_id=man_id, user=user, permissions=permissions)
		manager = Manager(man_id=man_id, user=user)
		manager.save()
		# manager.has_perm('can_add_restaurant')=1
		# manager.save()
		# permission = Permission(userid=man_id, can_add_restaurant=1)
		# permission.save()
		login(request, user)
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

# @permission_required('orders.can_add_restaurant')
# @permission_required('orders.can_vote')
@permission_required('can_add_restaurant')
def register_restaurant(request,pk):
	manager = Manager.objects.get(pk=pk)
	# if(request.user.has_perm('orders.add_restaurant')):
	# permission = Permission.objects.get(pk=pk)
	# if(permission.can_add_restaurant):
	if request.method == "POST":
		rest_id = request.POST['rest_id']
		name = request.POST['name']
		address = request.POST['address']
		city = request.POST['city']
		state = request.POST['state']
		country = request.POST['country']
		image = request.FILES['image']
		restaurant = Restaurant(rest_id=rest_id,name=name,address=address,city=city,state=state,country=country,image=image,man_id=manager)		
		restaurant.save()
		return redirect('reg_restaurant_home' , pk=restaurant.pk)
	else:
		return render(request, 'register_restaurant.html' , {'manager' : manager })
	# else:
	# 	return redirect('manager_home', pk=manager.man_id)

def reg_restaurant_home(request,pk):
	restaurant = get_object_or_404(Restaurant, pk=pk)
	items = Item.objects.filter(rest_id=pk)
	return render(request, 'reg_restaurant_home.html', {'restaurant': restaurant, 'items':items})

@permission_required('can_view_order')
def view_my_order(request,pk):
	customer = get_object_or_404(Customer, pk=pk)
	bills = Bill.objects.filter(cust_id=pk)
	return render(request, 'view_my_order.html', {'customer': customer, 'bills': bills})	

# @permission_required('can_add_item')
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

# @permission_required('can_view_restaurant')
def restaurant_home(request,pk):
	restaurant = get_object_or_404(Restaurant, pk=pk)
	items = Item.objects.filter(rest_id=pk)
	return render(request, 'restaurant_home.html', {'restaurant': restaurant, 'items':items, 'cust_id':request.user.customer.cust_id})	

		
def place_order(request, rest_id, cust_id):
	if request.method == "POST":
		customer = get_object_or_404(Customer, cust_id=cust_id)
		restaurant = get_object_or_404(Restaurant, rest_id=rest_id)
		bill_id = request.POST['bill_id']
		bill = Bill(bill_id=bill_id, rest_id=restaurant, cust_id=customer, total=0)
		bill.save()
		items = Item.objects.filter(rest_id=rest_id)
		bill = get_object_or_404(Bill, bill_id=bill_id)
		total=0
		for item in items:
			quantity = request.POST['quantity'+str(item.pk)]
			order = Order(bill_id=bill, item_id=item, quantity=quantity)
			total = total + item.cost*int(quantity)
			order.save()
		bill.total=total	
		bill.save()	
		return redirect('placed',pk=bill_id)
	else:
		return render(request, 'place_order.html')
		
def placed(request,pk):
	orders = Order.objects.filter(bill_id=pk)
	bill = get_object_or_404(Bill, bill_id=pk)
	return render(request,'placed.html',{'orders':orders,'bill':bill})

def placed_man(request,pk):
	orders = Order.objects.filter(bill_id=pk)
	bill = get_object_or_404(Bill, bill_id=pk)
	return render(request,'placed_man.html',{'orders':orders,'bill':bill})	

def bill_pdf(request, pk):
	orders = Order.objects.filter(bill_id=pk)
	bill = get_object_or_404(Bill, bill_id=pk)    
	html = loader.render_to_string('placed.html', {'orders':orders,'bill':bill})
	output = pdfkit.from_string(html, output_path=False)
	response = HttpResponse(content_type="application/pdf")
	response.write(output)
	return response


def restaurant_view_orders(request,pk):
	bills = Bill.objects.filter(rest_id=pk)
	return render(request,'restaurant_view_orders.html',{'bills':bills})

def search_by_city(request,pk):
	if request.method == "POST":
		customer = get_object_or_404(Customer, cust_id=pk)
		city = request.POST['city']
		if city:
			data = Restaurant.objects.filter(city=city)
			return render(request, 'customer_home.html', {'customer': customer,'restaurants': data})
		else:
			return redirect('customer_home',pk=pk)       
	else:
		return redirect('customer_home',pk=pk)

def search_by_name(request,pk):
	if request.method == "POST":
		customer = get_object_or_404(Customer, cust_id=pk)
		name = request.POST['name']
		if name:
			data = Restaurant.objects.filter(name=name)
			return render(request, 'customer_home.html', {'customer': customer,'restaurants': data})
		else:
			return redirect('customer_home',pk=pk)       
	else:
		return redirect('customer_home',pk=pk)

def delete_item(request, pk):
    item = get_object_or_404(Item, item_id=pk)
    rest_id = item.rest_id.rest_id
    item.delete()
    return redirect('reg_restaurant_home', pk=rest_id)

def feedback(request,rest_id,cust_id,bill_id):
	if request.method == "POST":
		customer = get_object_or_404(Customer, cust_id=cust_id)
		restaurant = get_object_or_404(Restaurant, rest_id=rest_id)
		feed_back = request.POST['feed_back']
		feed_back = Feedback(feed_back=feed_back,rest_id=restaurant,cust_id=customer)
		feed_back.save()
		return redirect('placed',pk=bill_id)
	else:
		customer = get_object_or_404(Customer, cust_id=cust_id)
		restaurant = get_object_or_404(Restaurant, rest_id=rest_id)
		bill = get_object_or_404(Bill, bill_id = bill_id)
		return render(request,'feedback.html',{'customer':customer,'restaurant':restaurant,'bill':bill})	


def feedback_man(request,pk):
	feedbacks = Feedback.objects.filter(rest_id=pk)
	return render(request, 'feedback_man.html', {'feedbacks':feedbacks})