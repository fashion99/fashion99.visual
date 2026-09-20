from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied

from .forms import MessageForm
from .models import Message
from accounts.decorators import feature_required
from accounts.models import User


@login_required
@feature_required('use_messaging')
def inbox(request):
	messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related('sender', 'recipient').order_by('-created_at')
	conversations = []
	seen_users = set()
	for item in messages:
		other_user = item.recipient if item.sender_id == request.user.id else item.sender
		if other_user.id in seen_users:
			continue
		seen_users.add(other_user.id)
		conversations.append({
			'user': other_user,
			'latest': item,
			'unread': Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).count(),
		})
	return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
@feature_required('use_messaging')
def compose(request, recipient_id=None):
	recipient = get_object_or_404(User, pk=recipient_id) if recipient_id else None
	form = MessageForm(request.POST or None, sender=request.user, recipient=recipient)
	if form.is_valid():
		message = form.save(commit=False)
		message.sender = request.user
		message.save()
		messages.success(request, 'Message sent.')
		return redirect('messaging:inbox')
	return render(request, 'messaging/compose.html', {'form': form})


@login_required
@feature_required('use_messaging')
def detail(request, pk):
	message = get_object_or_404(Message.objects.select_related('sender', 'recipient'), pk=pk)
	if message.sender_id != request.user.id and message.recipient_id != request.user.id:
		return redirect('messaging:inbox')
	other_user = message.sender if message.sender_id != request.user.id else message.recipient
	reply_data = request.POST.copy() if request.method == 'POST' else None
	if reply_data is not None:
		reply_data['recipient'] = other_user.pk
	reply_form = MessageForm(reply_data, sender=request.user, recipient=other_user)
	if request.method == 'POST' and reply_form.is_valid():
		reply = reply_form.save(commit=False)
		reply.sender = request.user
		reply.save()
		messages.success(request, 'Message sent.')
		return redirect('messaging:detail', pk=reply.pk)
	conversation = Message.objects.filter(sender__in=[request.user, other_user], recipient__in=[request.user, other_user]).select_related('sender').order_by('created_at')
	Message.objects.filter(recipient=request.user, sender=other_user, is_read=False).update(is_read=True)
	return render(request, 'messaging/detail.html', {'message': message, 'other_user': other_user, 'conversation': conversation, 'reply_form': reply_form})
    
def _can_manage_message(user, message, action):
	if message.sender_id == user.id:
		return getattr(user, f'can_{action}_own_messages', False) or user.is_admin_user()
	return getattr(user, f'can_{action}_all_messages', False) or user.is_admin_user()

@login_required
@feature_required('use_messaging')
def edit(request, pk):
	message = get_object_or_404(Message, pk=pk)
	if not _can_manage_message(request.user, message, 'edit'):
		raise PermissionDenied
	form = MessageForm(request.POST or None, instance=message, sender=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Message updated.')
		return redirect('messaging:detail', pk=message.pk)
	return render(request, 'messaging/compose.html', {'form': form, 'title': 'Edit message', 'submit_label': 'Save changes'})

@login_required
@feature_required('use_messaging')
def delete(request, pk):
	message = get_object_or_404(Message, pk=pk)
	if not _can_manage_message(request.user, message, 'delete'):
		raise PermissionDenied
	if request.method == 'POST':
		message.delete()
		messages.success(request, 'Message deleted.')
	return redirect('messaging:inbox')

# Create your views here.
