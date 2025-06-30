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
path('login',views.login,name='login'),
path('logout',views.logout,name='logout'),
path('me',views.me,name='me'),
path('borrowhistory',views.borrow_history,name='borrow_history'),
path('borrowaccept/<int:id>/',views.borrow_accept,name='borrow_accept'),
path('borrowreject/<int:id>/',views.borrow_reject,name='borrow_reject'),
path('addheads',views.add_head,name='add_head'),
path('addpmlead',views.Add_PM_Lead,name='Add_PM_Lead'),
path('edithead/<int:id>/',views.edit_head,name='edit_head'),
path('terminatehead/<int:id>/',views.terminate_head,name='terminate_head'),
path('editlead/<int:id>/',views.edit_lead,name='edit_lead'),
path('terminatelead/<int:id>/',views.terminate_lead,name='terminate_lead'),
path('searchstudent',views.search_student,name='search_student'),
path('blacklist',views.black_list,name='black_list'),
path('unblacklist/<int:id>/',views.un_blacklist,name='un_blacklist'),
]
