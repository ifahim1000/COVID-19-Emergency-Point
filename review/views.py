from django.shortcuts import redirect, render
from product.models import Product
from .models import Review

def WriteReview(request, id):
    if request.method == 'POST' :
        if request.user.is_authenticated :
            comment = request.POST['cmnt']
            product = Product.objects.get(id=id)
            rev = Review(user=request.user, product=product, comment=comment)
            rev.save()
            return redirect('/details/' + id)
        else :
            return redirect('/account/login')
        