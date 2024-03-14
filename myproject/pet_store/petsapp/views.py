from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Pet, Order, OrderItem, ShippingAddress, Customer, Customer1, Cartitem, ShippingAddress1, Order1, OrderItem1
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from .forms import signupform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .forms import ShippingAddress1Form, SetDeliveryAddressForm
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
import razorpay
# Create your views here.


def list_pets(request):
    object_list = Pet.objects.all()
    return render(request, 'petsapp/list.html', {'object_list': object_list})


def pet_detail(request, id):
    idd = Pet.objects.get(id=id)
    return render(request, 'petsapp/petdetail.html', {'data': idd})


def register(request):
    if request.method == 'POST':
        fn = UserCreationForm(request.POST)
        if fn.is_valid():
            u = fn.save()
            # uname = fn.cleaned_data['username']
            # upass = fn.cleaned_data['password1']
            # user = User.objects.create_user(username=uname, password=upass)
            # u = user.save()
            cus = Customer1.objects.create(user=u)
            print(cus)
            # print(uname)
            # print(upass)
            return redirect('/login_view')
    else:
        fn = UserCreationForm()
    return render(request, 'petsapp/signup.html', {'form': fn})


def user_login(request):
    if request.method == 'POST':
        fn = AuthenticationForm(request=request, data=request.POST)
        if fn.is_valid():
            uname = fn.cleaned_data['username']
            upass = fn.cleaned_data['password']
            u = authenticate(request.POST)
            return redirect('/list')
    else:
        fn = AuthenticationForm(request.POST)
    return render(request, 'petsapp/login.html', {'form': fn})


def user_logout(request):
    logout(request)
    return redirect('/login_view')


class SearchResultsView(ListView):
    model = Pet
    template_name = "petsapp/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Pet.objects.filter(
            Q(name__icontains=query) | Q(gender__icontains=query))
        return object_list


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=True)
        print(order)
        print(created)
        items = order.orderitem_set.all()
        print(items)
    else:
        items = []
    context = {'items': items, 'order': Order}
    return render(request, 'petsapp/cart.html', context)

    # if request.user.is_authenticated:
    #     try:
    #         customer = request.user.customer
    #     except Customer.DoesNotExist:
    #         # Handle the case where the user has no associated customer
    #         customer = None

    #     order, created = Order.objects.get_or_create(
    #         customer=customer, complete=True)
    #     print(order)
    #     print(created)
    #     items = order.orderitem_set.all()
    #     print(items)
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0}

    # context = {'items': items, 'order': order}
    # return render(request, 'petsapp/cart.html', context)


def checkout(request):
    return render(request, 'petsapp/checkout.html')

# revision class code


def add_to_cart(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    print(request.user)
    customer = Customer1.objects.get(user=request.user)
    existing_cart_items = Cartitem.objects.filter(
        customer=customer, pet=pet)
    if len(existing_cart_items) == 0:
        cart_item = Cartitem.objects.create(customer=customer, pet=pet)
    else:
        cart_item = existing_cart_items[0]
    cart_item.quantity = request.POST['quantity']
    cart_item.save()
    return redirect('cart_items')


def collect_cart_details(request):
    cart_items_list = Cartitem.objects.filter(customer__user=request.user)
    qty_list = [n for n in range(1, 6)]
    all_items_price = 0
    for item in cart_items_list:
        item.item_price = item.quantity*item.pet.price
        all_items_price = all_items_price+item.item_price
    context = {
        'cart': cart_items_list,
        'total_price': all_items_price,
        'qty_list': qty_list
    }
    return context


def cart_items(request):
    context = collect_cart_details(request)
    return render(request, 'petsapp/cart_items.html', context=context)


def remove_from_cart(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    cart_item = Cartitem.objects.get(customer__user=request.user.id, pet=pet)
    cart_item.delete()
    return redirect('cart_items')


def add_address(request):
    if request.method == 'POST':
        form = ShippingAddress1Form(request.POST)
        if form.is_valid():
            sd = form.save(commit=False)
            sd.customer = Customer1.objects.get(
                user__id=request.POST['customer'])
            sd.save()
            return redirect('order_review', sa_id=sd.id)
    else:
        form = ShippingAddress1Form()
    return render(request, 'petsapp/add_address.html', {'form': form})


def set_delivery_address(request):
    addr_list = ShippingAddress1.objects.filter(
        customer__user__id=request.user.id)
    if request.method == 'POST':
        form = SetDeliveryAddressForm(request.POST)
        if form.is_valid():
            return redirect('order_review', sa_id=form.cleaned_data['delivery_address'])
    else:
        form = SetDeliveryAddressForm()
    context = {
        'address_list': addr_list,
        'form': form
    }
    return render(request, 'delivery_address.html', context=context)


def order_review(request, sa_id):
    context = collect_cart_details(request)
    context['sa_id'] = ShippingAddress1.objects.get(id=sa_id)
    return render(request, 'petsapp/order_review.html', context=context)


def clear_cart_details(request):
    cart_items_list = Cartitem.objects.filter(customer__user=request.user)
    for item in cart_items_list:
        item.delete()


def checkout_order(request, sa_id):
    cart_items_list = collect_cart_details(request)['cart']
    customer = Customer1.objects.filter(user=request.user)
    delivery_addr = ShippingAddress1.objects.filter(id=sa_id)
    if customer:
        order = Order1(customer=customer[0], shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem1.objects.create(
                order=order, product=item.pet, price=item.pet.price, quantity=item.quantity)
            clear_cart_details(request)
            request.session['order_id'] = order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('list_pets'))


def payment_order(request):
    order_id = request.session.get('order_id')
    print("process_order order is -->", order_id)
    order = get_object_or_404(Order1, id=order_id)
    amount = int(order.get_total_cost()*100)
    amount_inr = amount
    context = {
        'order_id': order_id,
        'public_key': settings.RAZOR_KEY_ID,
        'amount': amount_inr,
        'amountring': amount
    }
    return render(request, 'petsapp/created.html', context=context)


client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payment_process(request, order_id, amount):
    order = get_object_or_404(Order1, id=order_id)
    if request.method == "POST":
        order.complete = True
        order.save()
        print("Amount ", amount)
        print("Type amount str to int ", amount)
        payment_id = request.POST['razorpay_payment_id']
        print("Payment Id", payment_id)
        order.transation_id = payment_id
        order.save()
        payment_client_capture = (client.payment.capture(payment_id, amount))
        print("Payment Client capture", payment_client_capture)
        payment_fetch = client.payment.fetch(payment_id)
        status = payment_fetch['status']
        amount_fetch = payment_fetch['amount']
        amount_fetch_inr = amount_fetch
        print("Payment Fetch", payment_fetch['status'])
        context = {
            'amount': amount_fetch_inr,
            'status': status,
            'transaction_id': payment_id
        }
        return render(request, 'petsapp/done.html', context=context)
