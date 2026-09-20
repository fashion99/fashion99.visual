from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	class Role(models.TextChoices):
		ADMIN = 'admin', 'Admin'
		STAFF = 'staff', 'Staff'

	role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
	can_view_dashboard = models.BooleanField(default=True)
	can_view_products = models.BooleanField(default=True)
	can_create_products = models.BooleanField(default=False)
	can_edit_products = models.BooleanField(default=False)
	can_delete_products = models.BooleanField(default=False)
	can_manage_stock = models.BooleanField(default=False)
	can_use_messaging = models.BooleanField(default=True)
	can_manage_accounts = models.BooleanField(default=False)
	can_message_admin = models.BooleanField(default=False)
	can_message_all = models.BooleanField(default=False)
	can_edit_own_messages = models.BooleanField(default=False)
	can_delete_own_messages = models.BooleanField(default=False)
	can_edit_all_messages = models.BooleanField(default=False)
	can_delete_all_messages = models.BooleanField(default=False)
	# Kept for compatibility with existing account data and migrations.
	can_edit_messages = models.BooleanField(default=False)
	can_delete_messages = models.BooleanField(default=False)

	def is_admin_user(self):
		return self.role == self.Role.ADMIN or self.is_superuser

	def has_feature_permission(self, feature):
		return self.is_superuser or self.is_admin_user() or getattr(self, f'can_{feature}', False)

# Create your models here.
