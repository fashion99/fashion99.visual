from django.db import migrations, models


def copy_message_permissions(apps, schema_editor):
	User = apps.get_model('accounts', 'User')
	User.objects.filter(can_edit_messages=True).update(can_edit_all_messages=True)
	User.objects.filter(can_delete_messages=True).update(can_delete_all_messages=True)


class Migration(migrations.Migration):

	dependencies = [
		('accounts', '0003_user_can_edit_messages_user_can_delete_messages'),
	]

	operations = [
		migrations.AddField(
			model_name='user',
			name='can_edit_own_messages',
			field=models.BooleanField(default=False),
		),
		migrations.AddField(
			model_name='user',
			name='can_delete_own_messages',
			field=models.BooleanField(default=False),
		),
		migrations.AddField(
			model_name='user',
			name='can_edit_all_messages',
			field=models.BooleanField(default=False),
		),
		migrations.AddField(
			model_name='user',
			name='can_delete_all_messages',
			field=models.BooleanField(default=False),
		),
		migrations.RunPython(copy_message_permissions, migrations.RunPython.noop),
	]