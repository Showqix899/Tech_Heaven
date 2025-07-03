from django.urls import path
from .views import place_order,single_order_placing

urlpatterns = [
        path('order/place/', place_order, name='place_order'),
        path('order/single/<uuid:item_id>/', single_order_placing, name='single_order_placing'),

]
