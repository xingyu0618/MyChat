from django.contrib.auth.models import AbstractUser
from django.db import models

from site2.utils import create_decimal_field

class Account(AbstractUser):
   balance = create_decimal_field()