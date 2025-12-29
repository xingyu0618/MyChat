from django.db import models


def create_decimal_field():
   return models.DecimalField(max_digits=12, decimal_places=2)