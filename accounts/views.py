from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccountCreateForm, AccountForm, PasswordResetForm
from .decorators import feature_required
from .models import User
from messaging.models import Message


def admin_required(view):
    return feature_required('manage_accounts')(view)


@login_required
@admin_required
def account_list(request):
    accounts = User.objects.order_by('username')
    for account in accounts:
        account.unread_message_count = Message.objects.filter(recipient=account, is_read=False).count()
    return render(request, 'accounts/list.html', {'accounts': accounts})


@login_required
@admin_required
def account_create(request):
    form = AccountCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account created.')
        return redirect('accounts:accounts')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Add account'})


@login_required
@admin_required
def account_edit(request, pk):
    account = get_object_or_404(User, pk=pk)
    form = AccountForm(request.POST or None, instance=account)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account updated.')
        return redirect('accounts:accounts')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Account settings'})


@login_required
@admin_required
def password_reset(request, pk):
    account = get_object_or_404(User, pk=pk)
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        account.set_password(form.cleaned_data['password'])
        account.save(update_fields=['password'])
        messages.success(request, 'Password updated.')
        return redirect('accounts:accounts')
    return render(request, 'accounts/password.html', {'form': form, 'account': account})


@login_required
@admin_required
def account_delete(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and account != request.user:
        account.delete()
    return redirect('accounts:accounts')
