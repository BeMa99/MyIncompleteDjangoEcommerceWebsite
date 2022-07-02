from django.test import TestCase
from MiApp import models
from django.core.files.images import ImageFile
from decimal import Decimal

class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        product = models.Products(name="This is Number 1", price=Decimal("10.00"),)
        product.save()
        with open("MiApp/static/images/img12.jpg", "rb")as f:
            image = models.ProductImage(product = product, image = ImageFile(f, name = "tctb.jpg"), )
            #AssertionError
            with self.assertLogs("MiApp", level = "INFO") as cm:
                image.save()
        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()
        with open("MiApp/static/images/img12.jpg", "rb",)as f:
            expected_content = f.read()
            assert image.thumbnail.read() == expected_content
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
