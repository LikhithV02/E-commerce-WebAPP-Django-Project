from django.shortcuts import render, redirect
from django.views import View
from .models import customer,category,cart,seller,product, order
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        fashion = product.objects.filter(category_id='2')
        electronics = product.objects.filter(category_id='1')
        books = product.objects.filter(category_id='3')
        grocery = product.objects.filter(category_id='4')
        return render(request, 'app/home.html',{'fashion': fashion, 'electronics':electronics,'books':books, 'grocery':grocery})


class ProductDetailView(View):
    def get(self, request, pk):
        pro = product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = cart.objects.filter(Q(Product=pro.pr_id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':pro, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    pro = product.objects.get(pr_id=product_id)
    cart(user=user, Product=pro).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        Cart = cart.objects.filter(user=user)
        #print(Cart)
        amount = 0.0
        shipping_amt = 120.0
        total_amt = 0.0
        cart_product = [p for p in cart.objects.all() if p.user==user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamt = (p.order_quantity * p.Product.pr_price)
                amount += tempamt
                total_amt = amount + shipping_amt
            return render(request, 'app/addtocart.html', {'carts': Cart, 'total_amt': total_amt
            , 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        #print(prod_id)
        c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user) )
        c.order_quantity+=1
        c.save()
        amount = 0.0
        shipping_amt = 120.0
        cart_product = [p for p in cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamt = (p.order_quantity * p.Product.pr_price)
            amount += tempamt

    data={
        'quantity': c.order_quantity,
        'amount': amount,
        'total_amt': amount + shipping_amt
    }
    return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
        c.order_quantity-=1
        c.save()
        amount = 0.0
        shipping_amt = 120.0
        cart_product = [p for p in cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamt = (p.order_quantity * p.Product.pr_price)
            amount += tempamt

    data={
            'quantity': c.order_quantity,
            'amount': amount,
            'total_amt': amount + shipping_amt
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amt = 120.0
        cart_product = [p for p in cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamt = (p.order_quantity * p.Product.pr_price)
            amount += tempamt

    data={
        'amount': amount,
        'total_amt': amount + shipping_amt
    }
    return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'c_add': add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = order.objects.filter(user_id=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

def electronics(request, data=None):
    if data==None:
        elec =product.objects.filter(category_id='1')
    elif data=='below':
        elec = product.objects.filter(category_id='1').filter(pr_price__lt=10000)
    elif data=='above':
        elec = product.objects.filter(category_id='1').filter(pr_price__gt=10000)
    return render(request, 'app/electronics.html', {'electronics':elec})

def fashion(request, data=None):
    if data==None:
        fash =product.objects.filter(category_id='1')
    elif data=='below':
        fash = product.objects.filter(category_id='1').filter(pr_price__lt=500)
    elif data=='above':
        fash = product.objects.filter(category_id='1').filter(pr_price__gt=500)
    return render(request, 'app/fashion.html', {'fashion':fash})

def books(request, data=None):
    if data==None:
        books =product.objects.filter(category_id='3')
    elif data=='below':
        books = product.objects.filter(category_id='3').filter(pr_price__lt=500)
    elif data=='above':
        books = product.objects.filter(category_id='3').filter(pr_price__gt=500)
    return render(request, 'app/books.html', {'books':books})


def grocery(request, data=None):
    if data==None:
        grocery =product.objects.filter(category_id='4')
    elif data=='below':
        grocery = product.objects.filter(category_id='4').filter(pr_price__lt=100)
    elif data=='above':
        grocery = product.objects.filter(category_id='4').filter(pr_price__gt=100)
    return render(request, 'app/grocery.html', {'grocery':grocery})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',
        {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = customer.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    amount = 0.0
    shipping_amt = 120.0
    total_amt = 0.0
    cart_product = [p for p in cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamt = (p.order_quantity * p.Product.pr_price)
            amount += tempamt
        total_amt += amount + shipping_amt
    return render(request, 'app/checkout.html', {'add':add, 'total_amt':total_amt, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user_ = request.user
    #user_id = request.user.pk
    cust_id = request.GET.get('custid')
    custom = customer.objects.get(c_id=cust_id)
    Cart = cart.objects.filter(user=user_)
    for c in Cart:
        order(user_id=user_, Customer=custom, Product=c.Product, cart_quantity=c.order_quantity).save()
        #orders.save()
        #custom.product.add(c.order_quantity, c.order_no, user_, c.Product, through_defaults={'order_date': 2})
        c.delete()
    return render(request, 'app/successfullorder.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['c_name']
            email = form.cleaned_data['email_id']
            mobile_no = form.cleaned_data['mobile_no']
            customer_address = form.cleaned_data['c_add']
            reg = customer(user = usr, c_name=name, email_id=email, mobile_no=mobile_no, c_add=customer_address)
            reg.save()
            messages.success(request, 'Congratulations!!! Profile has been Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

