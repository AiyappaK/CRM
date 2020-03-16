from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from .forms import orderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import orderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user,admin_only
from django.contrib.auth.models import Group
# inlineformset_factory they makes multiple forms using one form
@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    customerv = request.user.customer
    form = CustomerForm(instance=customerv)

    if request.method == 'POST':
        form = CustomerForm(request.POST ,request.FILES, instance=customerv)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status='deliverd').count()
    total_pending = orders.filter(status='Pending').count()

    context= {'orders':orders, 'total_orders':total_orders,
    'total_delivered':total_delivered,'total_pending':total_pending}
    return render(request, 'accounts/user.html',context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if  request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user =form.save()
            username = form.cleaned_data.get('username')
            group =Group.objects.get(name = 'customer')
            user.groups.add(group)
            customer.objects.create(
            user = user
            )
            messages.success(request,'Accounts was created for' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
    context = {}
    return render(request, 'accounts/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = order.objects.all()
    customers = customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    total_delivered = orders.filter(status='deliverd').count()
    total_pending = orders.filter(status='Pending').count()

    context = {'Orders' : orders,
               'customers' : customers,
    'total_orders': total_orders,
     'total_delivered' :total_delivered,
     'total_pending': total_pending
    }
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def product(request):
    product = products.objects.all()

    return render(request, 'accounts/products.html',{'products':product})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def Customer(request, pk_test):
    Customer = customer.objects.get(id=pk_test)
    orders = Customer.order_set.all()
    # total_orders = orders.count()
    myFilter = orderFilter( request.GET, queryset=orders)
    order = myFilter.qs

    context = {'customer':Customer, 'orders':orders, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(customer, order, fields=('products', 'status'),extra=10)
    # Customer, Order are realtion tables
    Customer = customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=order.objects.none(),instance=Customer)
    # form = orderForm(initial={'customer':Customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=Customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'accounts/ordder_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    Order = order.objects.get(id=pk)
    form = orderForm(instance=Order)
    if request.method == 'POST':
        form = orderForm(request.POST,instance=Order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/ordder_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    Order = order.objects.get(id=pk)
    if request.method == "POST":
        Order.delete()
        return redirect('/')

    context={'item':Order}
    return render(request,'accounts/delete.html',context)
