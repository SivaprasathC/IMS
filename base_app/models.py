from django.db import models

# Create your models here.

class Item(models.Model):
    serialno = models.CharField(max_length=100, unique=True)
    itemname = models.CharField(max_length=100)
    itemdomain = models.CharField(max_length=100)
    itemqty = models.IntegerField()
    itemimg = models.ImageField(upload_to='items/', blank=True, null=True)

    