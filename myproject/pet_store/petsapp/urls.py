from django.urls import path, include
from . import views
from .views import SearchResultsView
urlpatterns = [
    path('list', views.list_pets, name='list_pets'),
    path('<int:id>', views.pet_detail, name='petdetail'),
    path('login_view', views.user_login, name='login_view'),
    path('signup_view', views.register),
    path('logout_view', views.user_logout),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('add_to_cart/<int:pet_id>', views.add_to_cart, name='add_to_cart'),
    path('cart_items', views.cart_items, name='cart_items'),
    path('remove_from_cart/<int:pet_id>',
         views.remove_from_cart, name="remove_from_cart"),
    path('add_address', views.add_address, name='add_address'),
    path('set_delivery_address', views.set_delivery_address,
         name='set_delivery_address'),
    path('order_review/<int:sa_id>', views.order_review, name='order_review'),
    path('checkout_order/<int:sa_id>',
         views.checkout_order, name='checkout_order'),
    path('payment_order/', views.payment_order, name='payment_order'),
    path('payment_process/<int:order_id>/<int:amount>',
         views.payment_process, name="payment_process")
]
