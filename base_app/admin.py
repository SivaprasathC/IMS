from django.contrib import admin
from base_app.models import Item
from base_app.models import BorrowRequest
# Register your models here.

admin.site.register(Item)
admin.site.register(BorrowRequest)