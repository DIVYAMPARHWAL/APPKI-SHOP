from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateUserForm, OrderForm, ProductForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import company as Company, Item as Product, category as Category, Order,Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from .decorators import unauthenticated_user, allowed_users
from django.db.models import Sum
from django.utils import timezone
import datetime
from dateutil import rrule
from dateutil.relativedelta import relativedelta

def get_months_between_dates(start_date, end_date):
    months = []
    while start_date <= end_date:
        months.append(start_date.strftime("%B"))
        start_date += relativedelta(months=1)
    return months

@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop', 'employee'])
def index(request):
    product = Product.objects.all()
    group=request.user.groups.all()[0].name
    if group == 'employee':
        emp_id=Employee.objects.get(user=request.user)
        company_id=Company.objects.get(id=emp_id.company.id)
    else:
        company_id = Company.objects.get(user=request.user)
    product = Product.objects.all().filter(company=company_id.id)
    product_count = product.count()
    order = Order.objects.all().filter(ordered=True , being_delivered=False )
    days=30
    current_date = datetime.date.today()
    passed_date = current_date - datetime.timedelta(days=int(days))
    date_list = [passed_date + datetime.timedelta(days=x) for x in range((current_date-passed_date).days)]
    months = get_months_between_dates(passed_date, current_date)
    print(months)
    total_sales = Order.objects.filter(ordered=True ,being_delivered=True).aggregate(Sum('payment__amount'))['payment__amount__sum']
    all_order=Order.objects.filter(ordered=True).order_by('ordered_date')
    print(all_order)
    order_count = order.count()
    employee = Employee.objects.all().filter(company=company_id.id)
    customer_count = employee.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('shop:dashboard-index')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'order': order,
        'product': product,
        'company':company_id,
        'product_count': product_count,
        'order_count': order_count,
        'customer_count': customer_count,
        'total_sales': total_sales,
        'date_list': date_list,
        'all_orders': all_order,
        'months':months,
    }
    return render(request, 'shop/dashboard/index.html', context)


@login_required(login_url='shop:account_login')
def products(request):
    product = Product.objects.all()
    group=request.user.groups.all()[0].name
    if group == 'employee':
        emp_id=Employee.objects.get(user=request.user)
        company_id=Company.objects.get(id=emp_id.company.id)
    else:
        company_id = Company.objects.get(user=request.user)
    product = Product.objects.all().filter(company=company_id.id)
    product_count = product.count()
    employee = Employee.objects.all().filter(company=company_id.id)
    customer_count = employee.count()
    order = Order.objects.all().filter(ordered=True , being_delivered=False )
    order_count = order.count()
    item = Product()
    product_quantity = Product.objects.filter(title='')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.company=company_id
            form.save()
            product_name = form.cleaned_data.get('title')
            messages.success(request, f'{product_name} has been added')
            return redirect('shop:dashboard-products')
    else:
        form = ProductForm()
    context = {
        'product': product,
        'form': form,
        'order': order,
        'company': company_id,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'shop/dashboard/products.html', context)


@login_required(login_url='shop:account_login')
def product_detail(request, pk):
    item = Product.objects.get(id=pk)
    context = {
        'item': item,
    }
    return render(request, 'shop/dashboard/products_detail.html', context)


@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop'])
def employee(request):
    company_id = Company.objects.get(user=request.user)
    employee = Employee.objects.all().filter(company=company_id.id)
    customer_count = employee.count()
    product = Product.objects.all().filter(company=company_id.id)
    product_count = product.count()
    order = Order.objects.all().filter(ordered=True , being_delivered=False )
    order_count = order.count()
    context = {
        'order': order,
        'employee': employee,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
        'company':company_id,
    }
    return render(request, 'shop/dashboard/employee.html', context)


@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop'])
def employee_detail(request, pk):
    company_id = Company.objects.get(user=request.user)
    employee = Employee.objects.all().filter(company=company_id.id)    
    customer_count = employee.count()
    product = Product.objects.all().filter(company=company_id.id)
    product_count = product.count()
    order = Order.objects.all().filter(ordered=True , being_delivered=False )
    order_count = order.count()
    customers = Employee.objects.get(id=pk)
    context = {
        'order': order,
        'customers': customers,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
        'company':company_id,

    }
    return render(request, 'shop/dashboard/customers_detail.html', context)


@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop'])
def product_edit(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect("shop:dashboard-products")
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'shop/dashboard/products_edit.html', context)

@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop'])
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.save()
            return redirect("shop:dashboard-products")
    else:
        form = ProductForm
    context = {
        'form': form,
    }
    return render(request, 'shop/dashboard/products.html', context)

@login_required(login_url='shop:account_login')
@allowed_users(allowed_roles=['shop'])
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('shop:dashboard-products')
    context = {
        'item': item
    }
    return render(request, 'shop/dashboard/products_delete.html', context)


class ItemDetailView(DetailView):
    model = Order
    template_name = "shop/dashboard/order_view.html"

class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            company_id = Company.objects.get(user=self.request.user)
            employee = Employee.objects.all().filter(company=company_id.id)
            customer_count = employee.count()
            product = Product.objects.all().filter(company=company_id.id)
            product_count = product.count()
            order = Order.objects.all().filter(ordered=True , being_delivered=False )
            order_count = order.count()

            context = {
                'order': order,
                'customer_count': customer_count,
                'product_count': product_count,
                'order_count': order_count,
                'company':company_id,
            }
            return render(self.request, 'shop/dashboard/order.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "you do not have any active order")
            return redirect("/")

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm
    company = Company()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='shop')
            user.groups.add(group)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            company.name = form.cleaned_data.get(
                'company_name')
            company.user = user
            company.save()

            messages.success(request, 'Account was created for ' + username)
            return redirect("shop:account_login")

    context = {'form': form}
    return render(request, 'shop/partials/signup.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:shop-index')
        else:
            messages.info(request, 'username or password is incorrect')

    return render(request, 'shop/partials/login.html')


def logoutUser(request):
    logout(request)
    return redirect('shop:account_login')
