from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
PERMISSION_FIELDS = [
    'can_view_dashboard', 'can_view_products', 'can_create_products', 'can_edit_products',
    'can_delete_products', 'can_manage_stock', 'can_use_messaging', 'can_manage_accounts',
    'can_message_admin', 'can_message_all',
    'can_edit_own_messages', 'can_delete_own_messages', 'can_edit_all_messages',
    'can_delete_all_messages',
]

PERMISSION_LABELS = {
    'can_message_admin': 'Message admins',
    'can_message_all': 'Message all users',
    'can_edit_own_messages': 'Edit own messages',
    'can_delete_own_messages': 'Delete own messages',
    'can_edit_all_messages': 'Edit all messages',
    'can_delete_all_messages': 'Delete all messages',
}


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active'] + PERMISSION_FIELDS
        labels = PERMISSION_LABELS


class AccountCreateForm(AccountForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned_data