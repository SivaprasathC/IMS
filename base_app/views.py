from django.shortcuts import render
from base_app.models import Item

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
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'viewitems.html', context)