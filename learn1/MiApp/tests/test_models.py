from django.test import TestCase
from decimal import Decimal
from MiApp import models

class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Products.objects.create(name = "the gates", price = Decimal("10.00"))
        models.Products.objects.create(name= "this quiet house", price=Decimal("10.00"))
        models.Products.objects.create(name= "Tale Tells", price=Decimal("2.00"), active=False)
        self.assertEqual(len(models.Products.objects.active()), 2)
