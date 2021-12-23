from account.models import Buyer
from django.shortcuts import redirect, render
from .models import Affiliate

def CreateAff(request) :
    if request.user.is_authenticated :
        user = Buyer.objects.get(user=request.user)
        code = str(user.user.id)+str(user.user.name[0])+str(user.user.name[0])
        aff = Affiliate(user=user, aff_id=code,total_sales=0, total_commission=0.0)
        aff.save()
        return redirect('/profile/user')
    else :
        return redirect('/account/login')