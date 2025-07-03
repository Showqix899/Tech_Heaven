from django.shortcuts import render,redirect
from .models import Product, Category, Color
from .forms import ProductForm, CategoryForm, ColorForm
from django.db.models import Q
from accounts.decorators import admin_required
from django.http import HttpResponse
from cart.forms import AddToCartForm


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
            Q(category__name__icontains=query)
        )
        

        # Debugging output
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
        add_to_cart_form = AddToCartForm(initial={'quantity': 1})  # Initialize form with default quantity
        return render(request, 'products/product_detail.html', {'product': product, 'add_to_cart_form': add_to_cart_form})
    except Product.DoesNotExist:
        return render(request, 'products/product_detail.html', {'error': 'Product not found.'})
    

# product create view
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # Set prev_price from cleaned_data if exists
            prev_price = form.cleaned_data.get('prev_price')
            if prev_price:
                product.prev_price = prev_price

            product.save()
            form.save_m2m()  # Save ManyToMany like colors
            return redirect('product_list')
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
                updated_product = form.save(commit=False)

                # Manually set prev_price if discount was applied
                prev_price = form.cleaned_data.get('prev_price')
                if prev_price:
                    updated_product.prev_price = prev_price

                updated_product.save()
                form.save_m2m()

                return render(request, 'products/product_update.html', {
                    'form': form,
                    'success': 'Product updated successfully!'
                })
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



#category add from
@admin_required
def category_add(request):
    message = None
    if request.method == 'POST':

        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Category added successfully!'
        
        form = CategoryForm()  # Reset the form after saving
        return render(request, 'products/category_add.html', {'form': form, 'message': message})
    else:
        form = CategoryForm()
    return render(request, 'products/category_add.html', {'form': form, 'message': message})


# color add form
@admin_required
def color_add(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()

        form = ColorForm()  # Reset the form after saving
        return render(request, 'products/color_add.html', {'form': form, 'message':'Color added successfully!'})
    else:
        form = ColorForm()
    return render(request, 'products/color_add.html', {'form': form})


#category and color list view
@admin_required
def list_categories_and_colors(request):
    categories = Category.objects.all()
    colors = Color.objects.all()

    return render(request, 'products/list.html', {'categories': categories, 'colors': colors})

# Delete category view
@admin_required
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return redirect("list_categories_and_colors")
        except Category.DoesNotExist:
            return HttpResponse('Category not found', status=404)
    return HttpResponse('Invalid method', status=405)


# Delete color view
@admin_required
def delete_color(request, color_id):
    if request.method == 'POST':
        try:
            color = Color.objects.get(id=color_id)
            color.delete()
            return redirect("list_categories_and_colors")
        except Color.DoesNotExist:
            return HttpResponse('Color not found', status=404)
    return HttpResponse('Invalid method', status=405)