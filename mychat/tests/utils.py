from django.core.management import call_command


def load_accounts_data():
   call_command('loaddata', 'accounts.yaml')