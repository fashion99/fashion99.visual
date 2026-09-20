from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import feature_required
from .models import Product, ProductImage
from .forms import ProductForm, StockAdjustmentForm

def product_list(request):
	query = request.GET.get('q', '').strip()
	status = request.GET.get('status', 'active')
	products = Product.objects.prefetch_related('images')
	if not request.user.is_authenticated or status == 'active':
		products = products.filter(is_active=True)
	elif status == 'inactive':
		products = products.filter(is_active=False)
	if query:
		products = products.filter(Q(name__icontains=query) | Q(code__icontains=query))
	context = {'products': products, 'query': query, 'status': status}
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		return render(request, 'products/_results.html', context)
	return render(request, 'products/list.html', context)


@login_required
@feature_required('create_products')
def product_create(request):
	form = ProductForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		product = form.save()
		for image in request.FILES.getlist('images'):
			ProductImage.objects.create(product=product, image=image)
		messages.success(request, 'Product saved.')
		return redirect('products:list')
	return render(request, 'products/form.html', {'form': form, 'title': 'Add product'})


@login_required
@feature_required('edit_products')
def product_edit(request, pk):
	product = get_object_or_404(Product, pk=pk)
	form = ProductForm(request.POST or None, request.FILES or None, instance=product)
	if form.is_valid():
		form.save()
		remove_ids = request.POST.getlist('remove_images')
		for image in product.images.filter(pk__in=remove_ids):
			image.image.delete(save=False)
			image.delete()
		for image in request.FILES.getlist('images'):
			ProductImage.objects.create(product=product, image=image)
		messages.success(request, 'Product updated.')
		return redirect('products:list')
	return render(request, 'products/form.html', {'form': form, 'title': 'Edit product', 'product': product})


@login_required
@feature_required('manage_stock')
def stock_adjust(request, pk):
	product = get_object_or_404(Product, pk=pk)
	form = StockAdjustmentForm(request.POST or None, product=product)
	if form.is_valid():
		product.stock_quantity += form.cleaned_data['quantity']
		product.save(update_fields=['stock_quantity', 'updated_at'])
		messages.success(request, 'Stock updated.')
		return redirect('products:list')
	return render(request, 'products/stock.html', {'form': form, 'product': product})


@login_required
@feature_required('delete_products')
def product_delete(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		product.delete()
		messages.success(request, 'Product deleted.')
	return redirect('products:list')
from django.shortcuts import render

# Create your views here.
