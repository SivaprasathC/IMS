from django.shortcuts import render
from base_app.models import Item
import os
from django.db.models import Q
from django.shortcuts import redirect

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
        success_message_context ={
            'message': '<div class="alert alert-success" role="alert">Item Added Successfully!</div>'
        }
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
    item.delete()
    return redirect('viewitems')

def edit_item(request, id):
    item = Item.objects.get(id=id)
    return render(request, 'edititem.html', {'item': item})

def update_item(request, id):
    if request.method == 'POST':
        item = Item.objects.get(id=id)
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
        success_message_context = {
            'message': '<div class="alert alert-success" role="alert">Item Updated Successfully!</div>'
        }
        return render(request, 'edititem.html', success_message_context)