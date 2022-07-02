from django.test import TestCase
#from rest_framework.response import Response
from django.urls import reverse
#import datetime
#from django.db import models
#from django.utils import timezone

# Create your tests here.
class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello.html')
        self.assertContains(response, "learn1")

    def test_aboutUs_page_works(self):
        response = self.client.get(reverse("/aboutUs/"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aboutUs.html')
        self.assertContains(response, "learn1")

    def test_thanks_page_works(self):
        response = self.client.get(reverse("/thanks/"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'thanks.html')
        self.assertContains(response, "learn1")

    def test_products_page_works(self):
        response = self.client.get(reverse("/products/"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')
        self.assertContains(response, "learn1")

    def test_products_page_returns_active(self):
        models.Products.objects.create(name="", slug="", price=Decimal(""),)
        models.Products.objects.create(name="", slug="", price=Decimal(""), active=False)
        response = self.client.get(reverse("/products/", kwargs={"tag":"all"}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "learn1")
        products_list = models.Products.objects.active().order_by("name")
        self.assertEqual(list(response.context["object_list"]),list(products_list),)

    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Products.objects.create(name="", slug="", price=Decimal(""),)
        cb.tags.create(name="", slug = "")
        models.Products.objects.create(name="", slug="", price=Decimal(""),)
        response = self.client.get(reverse("", kwargs={"tag":""}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "learn1")
        products_list = models.Products.objects.active().filter(tags_slug="").order_by("name")
        self.assertEqual(list(response.context["object_list"]),list(products_list),)
        self.assertTemplateUsed(response, 'products.html')
