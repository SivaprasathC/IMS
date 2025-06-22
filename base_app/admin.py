from django.contrib import admin
from base_app.models import Item
from base_app.models import BorrowRequest
from .models import CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(BorrowRequest)