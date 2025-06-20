from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('add_item', views.add_item, name='add_item'),
path('viewitems', views.viewitems, name='viewitems'),
path('delete/<int:id>/', views.delete_item, name='delete_item'),
path('edit/<int:id>/', views.edit_item, name='edit_item'),
path('borrowitem/<int:id>/', views.borrow_item, name='borrow_item'),
path('newborrowrequest', views.new_borrow_request, name='new_borrow_request'),
path('borrowrequests', views.borrow_requests_list, name='borrow_requests_list'),
]
