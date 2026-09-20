from django import forms

from accounts.models import User
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'subject': forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Subject'}),
        }

    def __init__(self, *args, sender=None, recipient=None, **kwargs):
        super().__init__(*args, **kwargs)
        available_users = User.objects.exclude(pk=getattr(sender, 'pk', None))
        if sender is not None and sender.is_admin_user():
            pass
        elif getattr(sender, 'can_message_all', False):
            pass
        elif getattr(sender, 'can_message_admin', False):
            available_users = available_users.filter(role=User.Role.ADMIN) | available_users.filter(is_superuser=True)
        else:
            available_users = available_users.none()
        if self.instance and self.instance.pk and self.instance.recipient_id:
            available_users = available_users | User.objects.filter(pk=self.instance.recipient_id)
        self.fields['recipient'].queryset = available_users.order_by('username').distinct()
        if recipient is not None:
            self.fields['recipient'].initial = recipient.pk
            self.fields['recipient'].widget = forms.HiddenInput()
            self.fields['subject'].widget.attrs.update({'placeholder': 'Subject (optional)'})
            self.fields['body'].widget.attrs.update({'placeholder': 'Write a message...'})