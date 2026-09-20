from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('accounts', '0004_user_message_permissions'),
	]

	operations = [
		migrations.AddField(
			model_name='user',
			name='can_message_admin',
			field=models.BooleanField(default=False),
		),
		migrations.AddField(
			model_name='user',
			name='can_message_all',
			field=models.BooleanField(default=False),
		),
	]