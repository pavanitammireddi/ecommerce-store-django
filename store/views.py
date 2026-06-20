from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product, Cart, Order
from django.contrib.auth.models import User


def home(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    order_count = 0

    if request.user.is_authenticated:
        order_count = Order.objects.filter(user=request.user).count()
    cart_count = 0

    if request.user.is_authenticated:
       cart_count = Cart.objects.filter(user=request.user).count()

    return render(request, 'home.html', {
        'products': products,
        'order_count': order_count,
        'cart_count': cart_count

    })

@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    user = request.user
    Cart.objects.create(
        user=user,
        product=product,
        quantity=1
    )

    return redirect('/')


def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {'product': product})
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
@login_required
def remove_from_cart(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.delete()

    return redirect('/cart/')
@login_required
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    user = request.user

    Order.objects.create(
        user=user,
        total_price=total
    )

    cart_items.delete()

    return redirect('/')
@login_required
def increase_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.quantity += 1

    cart_item.save()

    return redirect('/cart/')
@login_required
def decrease_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('/cart/')

def register_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(request, "Passwords do not match")

            return redirect('/register/')

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect('/register/')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully!")

        return redirect('/login/')

    return render(request, 'register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        else:

            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_user(request):

    logout(request)

    return redirect('/')

@login_required
def orders(request):

    user_orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {
        'orders': user_orders
    })