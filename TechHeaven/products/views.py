from django.shortcuts import render
from .models import Product
from .forms import ProductForm
from django.db.models import Q
from accounts.decorators import admin_required

# Create your views here.

#product list view
def product_list(request):

    try:
        products = Product.objects.all()

        return render(request, 'products/product_list.html', {'products': products})
    except Product.DoesNotExist:
        return render(request, 'products/product_list.html', {'error': 'No products found.'})
    


#product search view
def product_search(request):
    query = request.GET.get('q', '').strip()

    if query:  # Only search if query is not empty
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

        print("Query:", query)
        print("Matched products:", products)

    else:
        products = Product.objects.none()  # Return empty result set if query is blank

    if not products.exists():
        return render(request, 'accounts/error_message.html', {
            'message': f'No products found matching "{query}".'
        })

    return render(request, 'products/product_detail.html', {
        'products': products,
        'query': query
    })

# product detail view
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return render(request, 'products/product_detail.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, 'products/product_detail.html', {'error': 'Product not found.'})
    

# product create view
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductForm()
            success_message = 'Product created successfully!'
            return render(request, 'products/product_create.html', {'form': form,'success': success_message})
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})




# product update view
@admin_required
def product_update(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return render(request, 'products/product_update.html', {'form': form, 'success': 'Product updated successfully!'})
        else:
            form = ProductForm(instance=product)
        return render(request, 'products/product_update.html', {'form': form})
    except Product.DoesNotExist:
        return render(request, 'products/product_update.html', {'error': 'Product not found.'})
    

# product delete view
@admin_required
def product_delete(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            product.delete()
            return render(request, 'products/product_delete.html', {'success': 'Product deleted successfully!'})
        return render(request, 'products/product_delete.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, 'products/product_delete.html', {'error': 'Product not found.'})
