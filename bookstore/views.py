from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
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
    return render(request, 'bookstore/customer.html', {'customer': customer, 'order': order})

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