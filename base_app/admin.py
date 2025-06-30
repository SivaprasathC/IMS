from django.contrib import admin
from base_app.models import *
# Register your models here.
class SearchCustomUser(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'role', 'domain', 'roll_number')

class SearchBorrowRequest(admin.ModelAdmin):
    search_fields = ('borrow_itemname','borrower_roll','borrow_status')

class SearchItem(admin.ModelAdmin):
    search_fields = ('serialno','itemname')

admin.site.register(CustomUser,SearchCustomUser)
admin.site.register(Item,SearchItem)
admin.site.register(BorrowRequest,SearchBorrowRequest)
admin.site.register(Blacklist)