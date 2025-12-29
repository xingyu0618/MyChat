from decimal import Decimal

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView

from .account import Account
from ..utils import create_decimal_field

from datetime import datetime, timezone
from django.utils import timezone as django_timezone

class Transaction(models.Model):
   sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
   recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
   amount = create_decimal_field()
   created_at = models.DateTimeField(default=django_timezone.now)

   @property
   def created_at_human(self):
      now = datetime.now(timezone.utc)
      created_at = self.created_at
      days_ago = (now - created_at).days
      days_ago_names = {0: '今天', 1: '昨天', 2: '前天'}
      time = self.created_at.strftime('%H:%M')
      if name := days_ago_names.get(days_ago):
         return  f'{name} {time}'
      date = self.created_at.strftime('%m/%d')
      return f'{date} {time}'

   @property
   def amount_display(self):
      1

class TransferForm(forms.ModelForm):
   sender = forms.ModelChoiceField(
      Account.objects.all(),
      disabled=True,
      to_field_name='username',
      widget=forms.HiddenInput(),
   )
   recipient = forms.ModelChoiceField(
      Account.objects.all(),
      to_field_name='username',
      widget=forms.TextInput(),
   )
   class Meta:
      model = Transaction
      fields = ['recipient', 'amount']
      labels = dict(
         recipient='接收方',
         amount='金额'
      )

   def clean_amount(self):
      amt = self.cleaned_data['amount']
      if amt < Decimal(0.0):
         raise ValidationError('转账金额必须大于0')
      return amt

@method_decorator([csrf_exempt, login_required], 'dispatch')
class TransactionView(FormView):
   form_class = TransferForm
   template_name = 'transaction.html'
   success_url = '/transaction-logs'

   initial = dict(
      recipient='bob',
      amount='10',
   )

   def get_form_kwargs(self):
      kwargs = super().get_form_kwargs()
      kwargs['initial'].update(sender=self.request.user.username)
      kwargs['renderer'] = FormRenderer()
      return kwargs

   def form_valid(self, form):
      xfer = form.instance
      xfer.sender=self.request.user
      # execute_transfer(xfer)
      return super().form_valid(form)

@method_decorator([login_required], 'dispatch')
class TransactionListView(ListView):
   model = Transaction

   def get_queryset(self):
      from django.db.models import Q, Case, When, F

      user = self.request.user
      qs = (
         Transaction.objects
         .filter(Q(sender=user) | Q(recipient=user))
         .annotate(
            signed_amount=Case(
               When(sender=user, then=-F('amount')),
               default=F('amount'),
            )
         )
      )
      return qs

def execute_transfer(transfer):
   with transaction.atomic():
      sender = transfer.sender
      recipient = transfer.recipient
      amount = transfer.amount

      sender.balance -= amount
      recipient.balance += amount
      sender.save()
      recipient.save()
