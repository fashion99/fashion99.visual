from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Message


User = get_user_model()


class MessageWorkflowTests(TestCase):
	def setUp(self):
		self.sender = User.objects.create_user(username='sender', password='password')
		self.recipient = User.objects.create_user(username='recipient', password='password')
		self.sender.can_edit_own_messages = True
		self.sender.can_delete_own_messages = True
		self.sender.can_message_all = True
		self.sender.save(update_fields=['can_edit_own_messages', 'can_delete_own_messages', 'can_message_all'])
		self.recipient.can_message_all = True
		self.recipient.save(update_fields=['can_message_all'])
		self.message = Message.objects.create(
			sender=self.sender,
			recipient=self.recipient,
			subject='Original',
			body='Message body',
		)

	def test_unread_badge_and_detail_mark_messages_read(self):
		self.client.login(username='recipient', password='password')
		inbox = self.client.get('/messages/')

		self.assertEqual(inbox.context['unread_message_count'], 1)
		self.assertContains(inbox, '>1<')

		self.client.get(f'/messages/{self.message.pk}/')
		self.message.refresh_from_db()
		self.assertTrue(self.message.is_read)

	def test_sender_can_edit_and_delete_own_message(self):
		self.client.login(username='sender', password='password')
		response = self.client.post(
			f'/messages/{self.message.pk}/edit/',
			{'recipient': self.recipient.pk, 'subject': 'Updated', 'body': 'Changed'},
		)
		self.assertRedirects(response, f'/messages/{self.message.pk}/')
		self.message.refresh_from_db()
		self.assertEqual(self.message.subject, 'Updated')

		response = self.client.post(f'/messages/{self.message.pk}/delete/')
		self.assertRedirects(response, '/messages/')
		self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())

	def test_recipient_needs_global_permission_to_edit_or_delete(self):
		self.client.login(username='recipient', password='password')
		self.assertEqual(self.client.get(f'/messages/{self.message.pk}/edit/').status_code, 403)
		self.assertEqual(self.client.post(f'/messages/{self.message.pk}/delete/').status_code, 403)

	def test_conversation_reply_uses_current_recipient(self):
		self.client.login(username='recipient', password='password')
		response = self.client.post(f'/messages/{self.message.pk}/', {'subject': '', 'body': 'Reply'})
		self.assertEqual(response.status_code, 302)
		reply = Message.objects.exclude(pk=self.message.pk).get()
		self.assertEqual(reply.sender, self.recipient)
		self.assertEqual(reply.recipient, self.sender)

# Create your tests here.
