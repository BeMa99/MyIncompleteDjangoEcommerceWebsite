from django.core.management.base import BaseCommand
from collections import Counter
import csv
import os.path
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from MiApp import models

class Command(BaseCommand):
    help = 'Import products in Learn1'
    def add_arguments(self, parser):
        parser.add_argument("MiApp/fixtures/CSVF.csv", type=open)
        parser.add_argument("MiApp/static/images", type=str)
    def handle(self, *args, **options):#where the import logic will be
        self.stdout.write("Importing products")
        c = Counter()
        reader = csv.DictReader(options.pop("MiApp/fixtures/CSVF.csv"))
        for row in reader:
            product, created = models.Products.objects.get_or_create(name=row["name"], price=row["price"])
            product.description = row["description"]
            product.slug = slugify(row["name"])
            for import_tag in row["tags"].split("|"):
                tag, tag_created = models.ProductTag.objects.get_or_create(name=import_tag)
                product.tags.add(tag)
                c["tags"] += 1
                if tag_created:
                    c["tags_created"] += 1
                with open( os.path.join( options["MiApp/static/images"], row["image_filename"],),"rb",) as f:
                    image = models.ProductImage(product=product, image=ImageFile(f, name=row["image_filename"]),)
                    image.save()
                    c["images"] += 1
                product.save()
                c["products"] += 1
                if created:
                    c["products_created"] += 1
            self.stdout.write( "Products processed=%d (created=%d)" % (c["products"], c["products_created"]))
        self.stdout.write("Tags processed=%d (created=%d)" % (c["tags"], c["tags_created"]))
        self.stdout.write("Images processed=%d" % c["images"])
