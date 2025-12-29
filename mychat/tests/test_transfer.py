from decimal import Decimal

import pytest

from ..domains.account import Account
from ..domains.transfer import Transaction, TransferForm, apply_transfer
from .utils import load_accounts_data

@pytest.mark.django_db
def test_transfer_form():
   load_accounts_data()

   form = TransferForm()
   # rendered = str(form)
   # assert rendered == 'abc'

   form = TransferForm(dict(
      sender=1,
      recipient=2,
      amount='9.9'
   ))
   assert form.errors == {}
   assert form.cleaned_data == dict(
      sender=Account.objects.get(pk=1),
      recipient=Account.objects.get(pk=2),
      amount=Decimal('9.9')
   )

   form = TransferForm(dict(
      sender=1,
      recipient=2,
      amount='-0.1'
   ))
   assert form.errors == dict(
      amount=['转账金额必须大于0']
   )

@pytest.mark.django_db
def test_smoke(db):
   load_accounts_data()

   xfer = Transaction.objects.create(sender_id=1, recipient_id=2, amount=Decimal('10'))
   # xfer = Transfer(sender=alice, recipient=bob, amount=Decimal('10'))
   apply_transfer(xfer)

   assert Account.objects.get(pk=1).balance == Decimal('90')
   assert Account.objects.get(pk=2).balance == Decimal('110')
