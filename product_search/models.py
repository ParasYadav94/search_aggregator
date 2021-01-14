from django.db import models


# Create your models here.

# Fields - Product Name, URL, Image and Price 

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    image = models.URLField(blank=False)
    url = models.TextField(blank=True)
    price = models.IntegerField(blank=False)

    def __str__(self):
        return self.name
