from django.shortcuts import render
from base_app.models import Item,BorrowRequest,Blacklist
import os
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import localtime, now
from django.contrib.auth.models import User, auth
from base_app.models import CustomUser
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def add_item(request):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
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
       

@login_required
def viewitems(request):
    search_query = request.GET.get('search', '')
    filter_domain = request.GET.get('domain', '')
    items = Item.objects.all()
    if (request.user.domain):
          items = items.filter(itemdomain=request.user.domain)
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

@login_required
def delete_item(request, id):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    item = Item.objects.get(id=id)
    item_name = item.itemname
    item.delete()
    message = item_name + ' has been deleted successfully!'
    messages.success(request, message)
    return redirect('viewitems')

@login_required
def edit_item(request, id):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    
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
                messages.error(request,'Invalid file type of Image!')
                return redirect('edit_item',id=id)
            item.itemimg = image
        
        item.save()
        messages.success(request, 'Your Edit was successful!')
        return redirect('viewitems')
    else:
        return render(request, 'edititem.html', {'item': item})

@login_required
def borrow_item(request, id):
    if request.user.role not in ["Student"]:
        return render(request,'error404.html')
    
    item = Item.objects.get(id=id)
    return render(request, 'borrowitem.html', {'item': item})

@login_required
def new_borrow_request(request):
    if request.user.role not in ["Student"]:
        return render(request,'error404.html')
    
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
        borrowqty = int(borrowqty)

        if Blacklist.objects.filter(studentroll=borrower_roll).exists():
            blacklisted = Blacklist.objects.get(studentroll=borrower_roll)
            context= "You are Blacklisted by "+blacklisted.blocked_by+"."+"<br>"+"<strong> Reason: </strong>"+blacklisted.block_reason
            messages.error(request, context)
            return redirect('viewitems')


      #only will submit request if qty available at that time(to avoid multiple users placing request)
        item= Item.objects.get(serialno = borrow_serialno)
        if (item.itemqty >= borrowqty):
            item.itemqty = item.itemqty-borrowqty
            item.save()
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
        else:
                messages.error(request, 'Item is currently Out of Stock!')
                return redirect('viewitems')

@login_required
def borrow_requests_list(request):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    search_query = request.GET.get('search_roll', '')
    user_domain = request.user.domain 
    borrow_requests = BorrowRequest.objects.all()
    # search func mixed with domain filter based on domain head or drh domain and only pending
    if search_query:
        borrow_requests = borrow_requests.filter(Q(borrower_roll__icontains=search_query))
    if user_domain:
        borrow_requests = borrow_requests.filter(
            Q(borrow_itemdomain=user_domain) & Q(borrow_status="Pending")
        )
    else:
        borrow_requests = borrow_requests.exclude(Q(borrow_status="Approved") | Q(borrow_status="Rejected") | Q(borrow_status="Returned"))
        print(borrow_requests)
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


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def me(request):
    return render(request,'profile.html')

@login_required
def borrow_history(request):
    if request.user.role not in ["Student"]:
        return render(request,'error404.html')
    
    borrow_requests = BorrowRequest.objects.filter(borrower_roll=request.user.roll_number)
    pending_requests = borrow_requests.filter(borrow_status="Pending")
    approved_requests = borrow_requests.filter(borrow_status="Approved")
    rejected_requests = borrow_requests.filter(borrow_status="Rejected")
    has_requests = pending_requests.exists() or approved_requests.exists() or rejected_requests.exists()
    return render(request, 'borrowhistory.html', {'pending_requests': pending_requests,'approved_requests': approved_requests,'rejected_requests': rejected_requests,'has_requests':has_requests})

@login_required
def borrow_accept(request,id):
      if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
      
      borrow_request = BorrowRequest.objects.get(id=id)
      if(request.user.role == "Lead" or request.user.role == "Super User" ):
            borrow_request.is_Lead_approved = True
            borrow_request.borrow_status = "Approved"
            borrow_request.save()
      elif (request.user.role == "Product Manager"):
             borrow_request.is_pm_approved = True
             borrow_request.borrow_status = "Approved"
             borrow_request.save()
      elif (request.user.role == "Domain Head"):
              borrow_request.is_dh_approved = True
              if(borrow_request.is_drh_approved == True):
                    borrow_request.borrow_status = "Approved"
              borrow_request.save()
      elif (request.user.role == "Domain Resource Head"):
              borrow_request.is_drh_approved = True
              if(borrow_request.is_dh_approved == True):
                  borrow_request.borrow_status = "Approved"
              borrow_request.save()
      messages.success(request, 'Request Approved Successfully!')
      return redirect('borrow_requests_list')


@login_required
def borrow_reject(request,id):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    
    if request.method == 'POST':
            borrow_request = BorrowRequest.objects.get(id=id)
            rejection_reason = request.POST.get('rejection_reason')
            borrow_request.borrow_status = "Rejected"
            borrow_request.rejection_reason = rejection_reason
            borrow_request.rejectedby = request.user.first_name+"-"+request.user.role
            borrow_request.save()

            itemserialno = request.POST.get('itemserialno')
            borrowqty = request.POST.get('borrowqty')
            item = Item.objects.get(serialno = itemserialno)
            item.itemqty = item.itemqty + int(borrowqty)
            item.save()
            messages.success(request, 'Request Rejected Successfully!')
            return redirect('borrow_requests_list')
    

@login_required
def add_head(request):
     if request.user.role not in ["Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
     if request.method == 'POST':
        first_name = request.POST.get('first_name')
        roll_number = request.POST.get('roll_number')
        email = request.POST.get('email')
        domain = request.POST.get('domain')
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not email.endswith('@kct.ac.in'):
            messages.error(request, 'Please Use Your College Mail!')
            return redirect('add_head')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('add_head')

        new_head = CustomUser(
            first_name=first_name,
            roll_number=roll_number,
            email=email,
            domain=domain,
            role=role,
            username=username
        )
        new_head.set_password(password) 
        new_head.save()
        
        context = ( "User created successfully!"+"<br>"+
                   "Please share the below details to Head:<br>"+
                   "<strong>Username: </strong>" + username + "<br>"
                    "<strong>Password:</strong>" + password)
        messages.success(request, context)
        return redirect('add_head')
     else:
         Domains_Heads = CustomUser.objects.filter(role="Domain Head")
         Domains_Reso_Heads = CustomUser.objects.filter(role="Domain Resource Head")
         context = {'Domain_Heads':Domains_Heads,'Domain_Resource_Heads':Domains_Reso_Heads}
         return render(request,'addheads.html',context)


@login_required
def Add_PM_Lead(request):
    if request.user.role not in ["Lead","Super User"]:
        return render(request,'error404.html')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        roll_number = request.POST.get('roll_number')
        email = request.POST.get('email')
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not email.endswith('@kct.ac.in'):
            messages.error(request, 'Please Use Your College Mail!')
            return redirect('Add_PM_Lead')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('Add_PM_Lead')

        new_lead = CustomUser(
            first_name=first_name,
            roll_number=roll_number,
            email=email,
            role=role,
            username=username
        )
        new_lead.set_password(password) 
        new_lead.save()
        
        context = ( "User created successfully!"+"<br>"+
                   "Please share the below details to the Product Manager or Lead:<br>"+
                   "<strong>Username: </strong>" + username + "<br>"
                    "<strong>Password:</strong>" + password)
        messages.success(request, context)
        return redirect('Add_PM_Lead')
    else:
         LeadIncludingRequestLead = CustomUser.objects.filter(role="Lead")
         #will not show the same user who has been logged in
         Leads = LeadIncludingRequestLead.exclude(id=request.user.id)
         ProdManagers = CustomUser.objects.filter(role="Product Manager")
         context = {'Leads':Leads,'ProdManagers':ProdManagers}
         return render(request,'addPMLead.html',context)
    
@login_required
def edit_head(request,id):
    if request.user.role not in ["Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        roll_number = request.POST.get('roll_number')
        email = request.POST.get('email')
        domain = request.POST.get('domain')
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not email.endswith('@kct.ac.in'):
            messages.error(request, 'Please Use Your College Mail!')
            return redirect('edit_head',id=id)
        
        #to avoid username already exists if unchanged in edit.
        users_without_current_user=CustomUser.objects.exclude(id=id)
        if users_without_current_user.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('edit_head',id=id)
        
        head = CustomUser.objects.get(id=id)
        head.first_name=first_name
        head.roll_number=roll_number
        head.email=email
        head.domain=domain
        head.role=role
        head.username=username
        if password:
            head.set_password(password) 
        head.save()
        context ="User Edited successfully!"
        messages.success(request, context)
        return redirect('add_head')
    else:
       head = CustomUser.objects.get(id=id)
       return render(request,'editheads.html',{'head':head})

@login_required
def terminate_head(request,id):
    if request.user.role not in ["Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    head = CustomUser.objects.get(id=id)
    headname = head.first_name
    head.delete()
    message = "<strong>"+headname + '</strong> has been terminated successfully!'
    messages.success(request, message)
    return redirect('add_head')
     


@login_required
def edit_lead(request,id):
    if request.user.role not in ["Lead","Super User"]:
        return render(request,'error404.html')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        roll_number = request.POST.get('roll_number')
        email = request.POST.get('email')
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not email.endswith('@kct.ac.in'):
            messages.error(request, 'Please Use Your College Mail!')
            return redirect('edit_lead',id=id)
        
        users_without_current_user=CustomUser.objects.exclude(id=id)
        if users_without_current_user.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('edit_lead',id=id)
        
        PMLead = CustomUser.objects.get(id=id)
        PMLead.first_name=first_name
        PMLead.roll_number=roll_number
        PMLead.email=email
        PMLead.role=role
        PMLead.username=username
        if password:
            PMLead.set_password(password) 
        PMLead.save()
        context ="User Edited successfully!"
        messages.success(request, context)
        return redirect('Add_PM_Lead')
    else:
        PMLead = CustomUser.objects.get(id=id)
        return render(request,'editPMLead.html',{'PMLead':PMLead})

@login_required
def terminate_lead(request,id):
    if request.user.role not in ["Lead","Super User"]:
        return render(request,'error404.html')
    PMLead = CustomUser.objects.get(id=id)
    PMLeadName = PMLead.first_name
    PMLead.delete()
    message = "<strong>"+PMLeadName + '</strong> has been terminated successfully!'
    messages.success(request, message)
    return redirect('Add_PM_Lead')

@login_required    
def search_student(request):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    if request.method == 'POST':
         roll_number = request.POST.get('roll_number')
         borrow_history = BorrowRequest.objects.filter(borrower_roll=roll_number)
         norequests= False
         if not borrow_history:
             norequests=True
         return render(request, 'searchstudent.html', {'borrow_history': borrow_history,'norequests':norequests})
    else:
         return render(request, 'searchstudent.html')
    

@login_required 
def black_list(request):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    if request.method=='POST':
        studentroll = request.POST.get('studentroll')
        block_reason = request.POST.get('block_reason')
        blockedby = request.user.first_name + " - "+request.user.role

        blacklist = Blacklist(
            studentroll =  studentroll ,
            block_reason = block_reason,
            blocked_by =  blockedby
        )
        blacklist.save()
        messages.success(request,'Student '+studentroll+' has been blacklisted successfully!')
        return redirect('black_list')
    else:
        blacklisted_students = Blacklist.objects.all()
        return render(request, 'blacklist.html', {'blacklisted_students': blacklisted_students})



@login_required
def un_blacklist(request,id):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    Blacklist.objects.filter(id=id).delete()
    messages.success(request, "Student has been removed from the blacklist")
    return redirect('black_list')

@login_required
def mark_return(request):
    if request.user.role not in ["Domain Head","Domain Resource Head","Lead","Product Manager","Super User"]:
        return render(request,'error404.html')
    
    return render(request,'markreturn.html')
