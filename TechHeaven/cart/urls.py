from django.urls import path
from .views import add_to_cart, view_cart, remove_cart_item
urlpatterns = [
    path('cart/add/<uuid:product_id>/',add_to_cart , name='add_to_cart'),
    path('cart/', view_cart, name='cart_view'),
    path('cart/remove/<uuid:item_id>/', remove_cart_item, name='remove_cart_item'),
]
