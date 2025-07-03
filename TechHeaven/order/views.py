from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import CartItem, Cart  # Adjust as needed
from cart.views import get_cart  # Assuming you use this helper
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


@login_required
def place_order(request):
    cart= get_cart(request)

    cart_items = cart.items.all()
    if not cart_items:
        return render(request, 'accounts/error_message.html', {
            'message': 'Your cart is empty. Please add items to your cart before placing an order.'
        })
    
    order= Order.objects.create(user=request.user)

    total = 0

    for item in cart_items:

        subtoral = item.product.price * item.quantity
        total += subtoral


        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
    order.total_amount = total
    order.save()

    # Clear the cart after placing the order
    cart.items.all().delete()
    return render(request, 'order/order_success.html', {
        'order': order,
        'total_amount': total
    })
    # return HttpResponse(f"Order placed successfully! Total amount: ${total:.2f}. Your order ID is {order.id}.")


#single order placing
@login_required
def single_order_placing(request, item_id):

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    order= Order.objects.create(user=request.user)
    total_price = cart_item.total_price()
    OrderItem.objects.create(
        order=order,
        product=cart_item.product,
        quantity=cart_item.quantity,
        price_at_order=total_price
    )
    order.total_amount = total_price
    order.save()

    # Clear the cart item after placing the order
    cart_item.delete()

    return HttpResponse(f"Order placed successfully for {cart_item.product.name}. Total amount: ${total_price:.2f}")