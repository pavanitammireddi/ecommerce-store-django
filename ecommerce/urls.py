from django.contrib import admin
from django.urls import path
from store.views import home, add_to_cart, product_detail, cart, remove_from_cart, place_order, increase_quantity, decrease_quantity, register_user, login_user, logout_user, orders

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),

    path('add-to-cart/<int:product_id>/', add_to_cart),

    path('product/<int:product_id>/', product_detail),

    path('cart/',cart),

    path('remove/<int:cart_id>/',remove_from_cart), 

    path('place-order/',place_order),

    path('increase/<int:cart_id>/',increase_quantity),

    path('decrease/<int:cart_id>/',decrease_quantity),

    path('register/', register_user),

    path('login/', login_user),

    path('logout/', logout_user),

    path('orders/',orders),
]