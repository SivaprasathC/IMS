from django.shortcuts import render
from base_app.models import Item,BorrowRequest
import os
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import localtime, now
from django.contrib.auth.models import User, auth
from base_app.models import CustomUser


# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_item(request):
    if request.method == 'GET':
         return render(request,'additem.html')

    if request.method == 'POST':
        serial_number = request.POST.get('serialno')
        name = request.POST.get('itemname')
        domain = request.POST.get('itemdomain')
        quantity = request.POST.get('itemqty')
        image = request.FILES.get('itemimg')

        if image: 
           valid_extensions = ['.jpeg', '.jpg', '.png']
           file_extension = os.path.splitext(image.name)[1].lower()
           if file_extension not in valid_extensions:
              error_message_context = {'message': '<div class="alert alert-danger" role="alert">Invalid file type of Image!</div>'}
              return render(request, 'additem.html', error_message_context)
            
        
        if Item.objects.filter(serialno=serial_number).exists():
            error_message_context = {
                'message': '<div class="alert alert-danger" role="alert">Serial Number already exists!</div>'
            }
            return render(request, 'additem.html', error_message_context)

        item = Item(
            serialno=serial_number,
            itemname=name,
            itemdomain=domain,
            itemqty=quantity,
            itemimg=image
        )
        item.save()
        success_message_context ={'message': '<div class="alert alert-success" role="alert">Item Added Successfully!</div>'}
        return render(request, 'additem.html', success_message_context)
       
def viewitems(request):
    search_query = request.GET.get('search', '')
    filter_domain = request.GET.get('domain', '')
    items = Item.objects.all()
    if search_query:
        items = items.filter(
            Q(itemname__icontains=search_query) | Q(serialno__icontains=search_query)
        )
    if filter_domain:
        items = items.filter(itemdomain=filter_domain)
    context = {
        'items': items
    }
    return render(request, 'viewitems.html', context)

def delete_item(request, id):
    item = Item.objects.get(id=id)
    item_name = item.itemname
    item.delete()
    message = item_name + ' has been deleted successfully!'
    messages.success(request, message)
    return redirect('viewitems')

def edit_item(request, id):
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        item.serialno = request.POST.get('serialno')
        item.itemname = request.POST.get('itemname')
        item.itemdomain = request.POST.get('itemdomain')
        item.itemqty = request.POST.get('itemqty')
        
        image = request.FILES.get('itemimg')
        if image:
            valid_extensions = ['.jpeg', '.jpg', '.png']
            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension not in valid_extensions:
                error_message_context = {'message': '<div class="alert alert-danger" role="alert">Invalid file type of Image!</div>'}
                return render(request, 'edititem.html', error_message_context)
            item.itemimg = image
        
        item.save()
        messages.success(request, 'Your Edit was successful!')
        return redirect('viewitems')
    else:
        return render(request, 'edititem.html', {'item': item})


def borrow_item(request, id):
    item = Item.objects.get(id=id)
    return render(request, 'borrowitem.html', {'item': item})

def new_borrow_request(request):
    if request.method == 'POST':
        borrower_userid = request.POST.get('borrower_userid')
        borrower_name = request.POST.get('borrower_name')
        borrower_roll = request.POST.get('borrower_roll')
        borrow_serialno = request.POST.get('borrow_serialno')
        borrow_itemname = request.POST.get('borrow_itemname')
        borrow_itemdomain = request.POST.get('borrow_itemdomain')
        borrowermobile = request.POST.get('borrowermobile')
        borrowreason = request.POST.get('borrowreason')
        borrowqty = request.POST.get('borrowqty')
        borrow_returndate = request.POST.get('borrow_returndate')
       
        time = localtime(now())

        new_request = BorrowRequest(
            
            borrower_userid=borrower_userid,
            borrower_name=borrower_name,
            borrower_roll=borrower_roll,
            borrow_serialno=borrow_serialno,
            borrow_itemname=borrow_itemname,
            borrow_itemdomain=borrow_itemdomain,
            borrowermobile=borrowermobile,
            borrowreason=borrowreason,
            borrowqty=borrowqty,
            borrow_returndate=borrow_returndate,
            borrow_made_date_time = time.strftime("%d/%m/%Y %H:%M")
        )
        new_request.save()
        messages.success(request, 'Borrow Request Submitted Successfully!')
        return redirect('viewitems')

def borrow_requests_list(request):
    search_query = request.GET.get('search_roll', '')
    borrow_requests = BorrowRequest.objects.all()
    borrow_requests=borrow_requests.filter(Q(borrower_roll__icontains=search_query))
    return render(request, 'borrow_requests_list.html', {'borrow_requests': borrow_requests})

def login(request):
    if request.method == 'POST' :
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(username=username,password=password)
       if user is None:
           messages.info(request,'Invalid Credentials! Please Contact the Product Manager or Lead')
           return redirect('login')
       else:
           auth.login(request,user)
           return redirect('/')
    else:   
       return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def me(request):
    return render(request,'profile.html')

def borrow_history(request):
    borrow_request = BorrowRequest.objects.filter(borrower_roll=request.user.roll_number)
    return render(request, 'borrowhistory.html', {'borrow_request': borrow_request})

