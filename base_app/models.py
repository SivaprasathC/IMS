from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Item(models.Model):
    serialno = models.CharField(max_length=100, unique=True)
    itemname = models.CharField(max_length=100)
    itemdomain = models.CharField(max_length=100)
    itemqty = models.IntegerField()
    itemimg = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return str(self.serialno)+'-'+str(self.itemname)+'-'+str(self.itemdomain)

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
    borrow_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),('Approved', 'Approved'), 
        ('Rejected', 'Rejected'),('Returned', 'Returned')],default='Pending') 
    is_Lead_approved = models.BooleanField(default=False)
    is_pm_approved = models.BooleanField(default=False)
    is_dh_approved = models.BooleanField(default=False)
    is_drh_approved = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=250,blank=True, null=True)
    borrow_made_date_time = models.CharField(max_length=50)
    is_returned = models.BooleanField(default=False)
    rejectedby = models.CharField(max_length=100,blank=True, null=True)
    is_damaged = models.BooleanField(default=False)
    damage_descp = models.CharField(max_length=250,blank=True, null=True)

    def __str__(self):
        return str(self.borrow_itemname)+'-'+str(self.borrower_roll)+'-'+str(self.borrow_status)

class CustomUser(AbstractUser):
    roll_number = models.CharField(max_length=50, unique=True,blank=True, null=True)
    role = models.CharField(max_length=50, choices=[
        ('Super User', 'Super User'),('Lead', 'Lead'), 
        ('Product Manager', 'Product Manager'),('Domain Head', 'Domain Head'),
        ('Domain Resource Head', 'Domain Resource Head'),('Student', 'Student')],blank=True, null=True)
    domain = models.CharField(max_length=50, blank=True, null=True,choices=[
        ('Domain 1', 'Domain 1'),('Domain 2', 'Domain 2'), 
        ('Domain 3', 'Domain 3'),('Domain 4', 'Domain 4'),
        ('Domain 5', 'Domain 5')])
    def __str__(self):
        return str(self.username)+'-'+str(self.first_name)+'-'+str(self.role)
    
class Blacklist(models.Model):
    studentroll = models.CharField(max_length=50,blank=True, null=True)
    block_reason=models.CharField(max_length=400,blank=True, null=True)
    blocked_by = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return str(self.studentroll)