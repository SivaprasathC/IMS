from django.db import models

# Create your models here.

class Item(models.Model):
    serialno = models.CharField(max_length=100, unique=True)
    itemname = models.CharField(max_length=100)
    itemdomain = models.CharField(max_length=100)
    itemqty = models.IntegerField()
    itemimg = models.ImageField(upload_to='items/', blank=True, null=True)

class BorrowRequest(models.Model):
    borrower_userid = models.CharField(max_length=50)
    borrower_name = models.CharField(max_length=100) 
    borrower_roll = models.CharField(max_length=50) 
    borrow_serialno = models.CharField(max_length=50) 
    borrow_itemname = models.CharField(max_length=100)
    borrow_itemdomain = models.CharField(max_length=50)
    borrowermobile = models.CharField(max_length=15)
    borrowreason = models.TextField()
    borrowqty = models.PositiveIntegerField()
    borrow_returndate = models.DateField() 
    borrow_status = models.CharField(max_length=20, default='Pending') 
    is_pm_approved = models.BooleanField(default=False)
    is_dh_approved = models.BooleanField(default=False)
    is_drh_approved = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=50,default='')
    borrow_made_date_time = models.CharField(max_length=50)