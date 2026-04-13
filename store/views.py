from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Category, Customer, Order, OrderItem, Product, ShippingAddress
from .forms import SignUpForm


def get_or_create_customer(user):
    customer, _ = Customer.objects.get_or_create(
        user=user,
        defaults={
            'name': user.get_full_name() or user.username,
            'email': user.email,
        }
    )
    return customer


def get_safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return None


def resolve_login_username(identifier):
    identifier = (identifier or '').strip()

    if not identifier:
        return ''

    user = User.objects.filter(username__iexact=identifier).first()
    if user:
        return user.username

    email_matches = User.objects.filter(email__iexact=identifier)
    if email_matches.count() == 1:
        return email_matches.first().username

    return identifier


# ================= STORE PAGE =================
def store(request):
    if request.user.is_authenticated:
        get_or_create_customer(request.user)

    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(title__icontains=search_query)

    # Category filter
    cat_id = request.GET.get('category')
    if cat_id:
        products = products.filter(category_id=cat_id)

    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'page_obj': page_obj
    }

    return render(request, 'store/store.html', context)


# ================= PRODUCT DETAIL =================
def product_detail(request, product_id):
    if request.user.is_authenticated:
        get_or_create_customer(request.user)

    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


# ================= CART =================
def cart(request):
    if request.user.is_authenticated:
        customer = get_or_create_customer(request.user)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False
        )
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []

    return render(request, 'store/cart.html', {
        'items': items,
        'order': order
    })


# ================= CHECKOUT =================
@login_required
def checkout(request):
    customer = get_or_create_customer(request.user)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    items = order.orderitem_set.all()

    return render(request, 'store/checkout.html', {
        'order': order,
        'items': items,
        'customer': customer
    })


# ================= UPDATE CART =================
@login_required
def update_item(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')

    product = get_object_or_404(Product, id=product_id)
    customer = get_or_create_customer(request.user)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product
    )

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return redirect('cart')


# ================= PROCESS ORDER =================
@login_required
def process_order(request):
    transaction_id = request.POST.get('transaction_id')

    customer = get_or_create_customer(request.user)
    order = Order.objects.get(customer=customer, complete=False)

    order.transaction_id = transaction_id
    order.complete = True
    order.status = 'Paid'
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        zipcode=request.POST.get('zipcode'),
    )

    return redirect('store')


# ================= AUTH =================
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            Customer.objects.create(
                user=user,
                name=user.get_full_name() or user.username,
                email=user.email
            )

            login(request, user)
            messages.success(request, "Account created!")
            return redirect('store')
    else:
        form = SignUpForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store')

    next_url = get_safe_next_url(request)
    login_value = ''

    if request.method == 'POST':
        login_value = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        username = resolve_login_username(login_value)

        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            get_or_create_customer(user)
            return redirect(next_url or 'store')
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, 'store/login.html', {
        'next': next_url,
        'login_value': login_value,
    })


def logout_view(request):
    logout(request)
    return redirect('store')


# ================= ORDER HISTORY =================
@login_required
def order_history(request):
    customer = get_or_create_customer(request.user)
    orders = Order.objects.filter(
        customer=customer,
        complete=True
    ).order_by('-date_ordered')

    return render(request, 'store/order_history.html', {'orders': orders})


# ================= PROFILE =================
@login_required
def profile(request):
    customer = get_or_create_customer(request.user)
    addresses = ShippingAddress.objects.filter(customer=customer)
    orders = Order.objects.filter(customer=customer, complete=True)

    total_spent = sum(order.get_cart_total for order in orders)

    return render(request, 'store/profile.html', {
        'orders': orders,
        'addresses': addresses,
        'total_spent': total_spent
    })
