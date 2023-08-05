from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
# Create your views here.


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

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()

    searchFilter = OrderFilter(request.GET, queryset=order)
    order = searchFilter.qs

    return render(request, 'bookstore/customer.html', {'customer': customer,
                                                       'myFilter': searchFilter, 
                                                       'order': order,})

def profile(request):
    return render(request, 'bookstore/profile.html')

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

def delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'bookstore/delete_form.html', context)

def login(request):
    context = {}
    return render(request, 'bookstore/login.html', context)

def register(request):
    context = {}
    return render(request, 'bookstore/register.html', context)