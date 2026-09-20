from django.conf import settings
from django.db import models


class MessageType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)


class Message(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sent_messages')
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='received_messages')
	message_type = models.ForeignKey(MessageType, on_delete=models.SET_NULL, related_name='messages', null=True, blank=True)
	subject = models.CharField(max_length=255, blank=True)
	body = models.TextField(blank=True)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)


class StockUpdate(models.Model):
	message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='stock_update')
	product_code = models.CharField(max_length=100, db_index=True)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=12, decimal_places=2)

# Create your models here.
