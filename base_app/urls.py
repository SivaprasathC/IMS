from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('add_item', views.add_item, name='add_item'),
path('viewitems', views.viewitems, name='viewitems'),
path('delete/<int:id>/', views.delete_item, name='delete_item'),
path('edit/<int:id>/', views.edit_item, name='edit_item'),
]
