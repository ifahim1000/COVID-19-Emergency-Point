from product.models import Product
from affiliate.models import Affiliate
from django.shortcuts import redirect, render
from account.models import Buyer, CustomUser, Provider
from order.models import Order

def UserDashboard(request) :
    if request.user.is_authenticated :
        try :
            user = Buyer.objects.get(user=request.user)
        except Buyer.DoesNotExist :
            user = None
        if user is None :
            return redirect('/account/login')
        else :
            try :
                aff = Affiliate.objects.get(user=user)
            except Affiliate.DoesNotExist  :
                aff = None
            orders = Order.objects.filter(buyer=request.user)
            context = {
                'user' : user,
                'aff' : aff,
                'orders' : orders,
            }
            return render(request, 'user_profile.html', context)
    else :
        return redirect('/account/login')
    
def UpdateProfile(request) :
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        
        profile = CustomUser.objects.get(id=request.user.id)
        profile.name = name
        profile.email = email
        profile.phone = phone
        profile.address = address
        profile.save()
        
        if password :
            profile.set_password(password)
        
        return redirect('/profile/user')

def ProviderDashboard(request) :
    if request.user.is_authenticated :
        try :
            user = Provider.objects.get(user=request.user)
        except Provider.DoesNotExist :
            user = None
        if user is None :
            return redirect('/account/login')
        else :
            orders = Order.objects.filter(product__seller=request.user)
            customers = Order.objects.filter(product__seller=request.user).values_list('buyer').distinct()
            products = Product.objects.filter(seller=request.user)
            
            completed = 0
            due = 0
            inProgress = 0
            
            for order in orders :
                if order.status == "Delivered" :
                    completed+=1
                elif order.status == "In Progress" :
                    inProgress+=1
                else :
                    due += 1
            
            context = {
                'user' : user,
                'orders' : orders,
                'products' : products,
                'customers' : customers,
                'completed' : completed,
                'due' : due,
                'inProgress' : inProgress,
            }
            return render(request, 'provider_profile.html', context)
    else :
        return redirect('/account/login')

def UpdateProvider(request) :
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        company = request.POST['company']
        address = request.POST['address']
        password = request.POST['password']
        
        profile = CustomUser.objects.get(id=request.user.id)
        profile.name = name
        profile.email = email
        profile.phone = phone
        profile.address = address
        profile.company_name=company
        profile.save()
        
        if password :
            profile.set_password(password)
        
        return redirect('/profile/provider')
    
# py manage.py runserver