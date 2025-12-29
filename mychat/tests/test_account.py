import pytest

from .utils import load_accounts_data
from ..domains.account import Account


@pytest.mark.django_db
def test_smoke(db):
   load_accounts_data()
   alice = Account.objects.get(pk=1)
   bob = Account.objects.get(pk=2)
   assert alice.username == 'alice'
   assert bob.username == 'bob'
