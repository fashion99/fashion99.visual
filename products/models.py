from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=100, unique=True, db_index=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	stock_quantity = models.PositiveIntegerField(default=0)
	low_stock_threshold = models.PositiveIntegerField(default=5)
	is_active = models.BooleanField(default=True, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.name} ({self.code})'


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='products/')
	display_order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['display_order', 'created_at']

# Create your models here.
