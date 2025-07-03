from django.shortcuts import render

from .models import Cart, CartItem
from products.models import Product
from .forms import AddToCartForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect

# Create your views here.


#get cart 
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    return cart

#add to cart
@login_required
def add_to_cart(request,product_id):

    if not request.user.is_authenticated:
        return redirect('login')
    
    product=get_object_or_404(Product, id=product_id)

    form = AddToCartForm(request.POST)

    if form.is_valid():

        quantity = form.cleaned_data['quantity']
        cart = get_cart(request)
        item,created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if created:
            item.quantity=quantity
        else:
            item.quantity += quantity

        item.save()

        message = f"{product.name} has been added to your cart."

        return render(request, 'products/product_detail.html', {
            'message': message,
            'product': product,
            'add_to_cart_form': AddToCartForm(initial={'quantity': 1})
        })
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'add_to_cart_form': form,
        'message': 'Invalid quantity'
    })

#remove cart item
@login_required
def remove_cart_item(request, item_id):

    if not request.user.is_authenticated:
        return redirect('login')
    
    try:

        item = CartItem.objects.get(id=item_id)

        item.delete()
        print(f"Item {item_id} removed from cart.")
        return redirect('cart_view')
    
    except CartItem.DoesNotExist:
        print(f"Item {item_id} does not exist in the cart.")
        return redirect('view_cart')


#view cart
@login_required
def view_cart(request):
    cart = get_cart(request)

    return render(request, 'carts/view_cart.html', {
        'cart': cart,
    })