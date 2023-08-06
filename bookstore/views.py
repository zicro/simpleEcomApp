from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateNewUser, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import notLoggedUser, allowedUser, forAdmins
from django.contrib.auth.models import Group
# Create your views here.

@login_required(login_url='login')
@allowedUser(allowedGroups=['admin'])
def home(request):
    customers = Customer.objects.all()
    t_customers = customers.count()

    orders = Order.objects.all()
    t_orders = orders.count()
    p_orders = orders.filter(status = 'Pending').count()
    d_orders = orders.filter(status = 'Delivered').count()
    in_orders = orders.filter(status = 'in progress').count()
    out_orders = orders.filter(status = 'Out of Order').count()
    c_orders = orders.filter(status = 'Cancelled').count()

    context = {'customers': customers, 'orders': orders, 't_customers': t_customers,
               'p_orders': p_orders, 'd_orders': d_orders, 'in_orders': in_orders,
               'out_orders': out_orders, 'c_orders':c_orders, 't_orders': t_orders}

    return render(request, 'bookstore/dashboard.html', context)

def books(request):
    books = Book.objects.all()
    return render(request, 'bookstore/books.html', {'books': books})

@forAdmins
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()

    searchFilter = OrderFilter(request.GET, queryset=order)
    order = searchFilter.qs

    return render(request, 'bookstore/customer.html', {'customer': customer,
                                                       'myFilter': searchFilter, 
                                                       'order': order,})


def create(request):
    form = OrderForm()
    if request.method == 'POST':
        #print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'bookstore/my_order_form.html', context)

def creates(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('book', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    if request.method == 'POST':
        #print(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'bookstore/my_order_form.html', context)

@allowedUser(allowedGroups=['admin'])
def update(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'bookstore/my_order_form.html', context)

@allowedUser(allowedGroups=['admin'])
def delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'bookstore/delete_form.html', context)

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/logout')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'username or password not found..')
    context = {}
    return render(request, 'bookstore/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('login')

@notLoggedUser
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            gUser = form.save()
            user = form.cleaned_data.get('username')
            #group = Group.objects.get(name="customer")
            #gUser.groups.add(group)
            messages.success(request, 'User registration successful '+user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'bookstore/register.html', context)


@login_required(login_url='login')
@allowedUser(allowedGroups=['customer'])
def profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    orders = request.user.customer.order_set.all()
    # to update the user account profile
    if request.method == 'POST':
        form = CustomerForm( request.POST, request.FILES ,instance=customer)
        if form.is_valid():
            form.save()
    context = {'orders':orders, 'form':form}
    return render(request, 'bookstore/profile.html', context)