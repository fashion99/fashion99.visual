from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('accounts', '0002_user_can_create_products_user_can_delete_products_and_more'),
	]

	operations = [
		migrations.AddField(
			model_name='user',
			name='can_edit_messages',
			field=models.BooleanField(default=False),
		),
		migrations.AddField(
			model_name='user',
			name='can_delete_messages',
			field=models.BooleanField(default=False),
		),
	]