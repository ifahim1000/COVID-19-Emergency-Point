import decimal
from django.contrib import messages
from affiliate.models import Affiliate
from order.models import Order
from product.models import Product
from django.shortcuts import redirect, render

def MakeOrder(request, id) :
    if request.method == 'POST' :
        quantity = request.POST['quantity']
        code = request.POST['code']
        
        product = Product.objects.get(id=id)
        price = product.price * int(quantity)
        
        if code :
            try :
                aff = Affiliate.objects.get(aff_id = code)
            except Affiliate.DoesNotExist :
                aff = None
            if aff is None :
                messages.error(request, "Voucher code invalid.")
                return redirect('/details/'+id)
            else :
                aff.total_sales += 1
                aff.total_commission += decimal.Decimal(price)*decimal.Decimal(0.15)
                aff.save()
                price -= decimal.Decimal(price) * decimal.Decimal(0.10)
                messages.success(request, "Voucher applied successfully you got 10% discount")
        
        order = Order(buyer=request.user, product=product, quantity=quantity, price=price, status="Pending")
        order.save()
        
        messages.success(request, "Product ordered successfully.")
        return redirect('/details/'+id)
        