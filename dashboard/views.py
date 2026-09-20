from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render
from messaging.models import Message
from products.models import Product
from accounts.decorators import feature_required


@login_required
@feature_required('view_dashboard')
def home(request):
	context = {
		'active_products': Product.objects.filter(is_active=True).count(),
		'low_stock_products': Product.objects.filter(is_active=True, stock_quantity__lte=models.F('low_stock_threshold')).count(),
		'total_stock': Product.objects.filter(is_active=True).aggregate(total=models.Sum('stock_quantity'))['total'] or 0,
		'unread_messages': Message.objects.filter(recipient=request.user, is_read=False).count(),
	}
	return render(request, 'dashboard/home.html', context)
from django.shortcuts import render

# Create your views here.
