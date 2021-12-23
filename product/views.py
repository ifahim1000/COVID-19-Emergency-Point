from account.models import Buyer
from affiliate.models import Affiliate
from review.models import Review
from product.forms import ProductForm
from django.shortcuts import redirect, render
from geopy import distance
from .models import Product
from django.contrib import messages
from functools import cmp_to_key

import json

def CalculateDistance(lat1, long1, lat2, long2) :
    place1 = (lat1, long1)
    place2 = (lat2, long2)
    dis = distance.distance(place1, place2).m
    return dis

def HomePage(request) :
    if request.method == 'GET' :
        return render(request, 'home.html')

def AddProduct(request) :
    if request.method == 'POST' :
        form = ProductForm(request.POST, request.FILES)
        category = request.POST['dropdown']
        if form.is_valid() :
            frm = form.save(commit=False)
            frm.seller = request.user
            frm.stock = True
            frm.category = category
            frm.save()
            messages.success(request, "Product added successfully.")
            return redirect('/add-product')
        else :
            messages.error(request, "Error uploading image.")
            return redirect('/add-product')
    else :
        if request.user.is_authenticated:
            form = ProductForm()
        else :
            return redirect('/account/login')
    return render(request, 'add_product.html', {'form':form})

def MedicineProduct(request) :
    if request.method == 'GET' :
        data = request.GET
        lat = 0.0
        long = 0.0
        for d in data :
            json_data = json.loads(d)
            lat = json_data['latitude']
            long = json_data['longitude'] 

        product = Product.objects.raw("SELECT * FROM product_product INNER JOIN account_provider ON product_product.seller_id=account_provider.user_id AND product_product.category='Medicine'")
        qList = list(product)
        
        qList.sort(key=cmp_to_key(lambda x,y: 1 if CalculateDistance(lat,long,x.latitude,x.longitude)<CalculateDistance(lat,long,y.latitude,y.longitude) else -1))
        
        return render(request, 'medicine_products.html', {'products' : qList})

def IcuProduct(request) :
    if request.method == 'GET' :
        data = request.GET
        lat = 0.0
        long = 0.0
        for d in data :
            json_data = json.loads(d)
            lat = json_data['latitude']
            long = json_data['longitude'] 

        product = Product.objects.raw("SELECT * FROM product_product INNER JOIN account_provider ON product_product.seller_id=account_provider.user_id AND product_product.category='ICU'")
        qList = list(product)
        
        qList.sort(key=cmp_to_key(lambda x,y: 1 if CalculateDistance(lat,long,x.latitude,x.longitude)<CalculateDistance(lat,long,y.latitude,y.longitude) else -1))
        
        return render(request, 'icu_products.html', {'products' : qList})
    
def AmbulanceProduct(request) :
    if request.method == 'GET' :
        data = request.GET
        lat = 0.0
        long = 0.0
        for d in data :
            json_data = json.loads(d)
            lat = json_data['latitude']
            long = json_data['longitude'] 

        product = Product.objects.raw("SELECT * FROM product_product INNER JOIN account_provider ON product_product.seller_id=account_provider.user_id AND product_product.category='Ambulance'")
        qList = list(product)
        
        qList.sort(key=cmp_to_key(lambda x,y: 1 if CalculateDistance(lat,long,x.latitude,x.longitude)<CalculateDistance(lat,long,y.latitude,y.longitude) else -1))
        
        return render(request, 'ambulance_products.html', {'products' : qList})
    
def HospitalProduct(request) :
    if request.method == 'GET' :
        data = request.GET
        lat = 0.0
        long = 0.0
        for d in data :
            json_data = json.loads(d)
            lat = json_data['latitude']
            long = json_data['longitude'] 

        product = Product.objects.raw("SELECT * FROM product_product INNER JOIN account_provider ON product_product.seller_id=account_provider.user_id AND product_product.category='Hospital'")
        qList = list(product)
        
        qList.sort(key=cmp_to_key(lambda x,y: 1 if CalculateDistance(lat,long,x.latitude,x.longitude)<CalculateDistance(lat,long,y.latitude,y.longitude) else -1))
        
        return render(request, 'hospital_products.html', {'products' : qList})

def OxygenProduct(request) :
    if request.method == 'GET' :
        data = request.GET
        lat = 0.0
        long = 0.0
        for d in data :
            json_data = json.loads(d)
            lat = json_data['latitude']
            long = json_data['longitude'] 

        product = Product.objects.raw("SELECT * FROM product_product INNER JOIN account_provider ON product_product.seller_id=account_provider.user_id AND product_product.category='Oxygen'")
        qList = list(product)
        
        qList.sort(key=cmp_to_key(lambda x,y: 1 if CalculateDistance(lat,long,x.latitude,x.longitude)<CalculateDistance(lat,long,y.latitude,y.longitude) else -1))
        
        return render(request, 'hospital_products.html', {'products' : qList})

def ProductDetails(request, id) :
    if request.method == 'GET' :
        try :
            product = Product.objects.get(id=id)
        except Product.DoesNotExist :
            product = None
        reviews = Review.objects.filter(product=product)
        context = {
            'product' : product,
            'reviews' : reviews,
        }
        return render(request, 'product_details.html', context)

def SearchProducts(request) :
    if request.method == 'POST' :
        data = request.POST["searchText"]
        all_products = Product.objects.filter(name__contains=data) | Product.objects.filter(description__contains=data)
        context = {
            'search' : data,
            'all_products' : all_products,
        }
    return render(request, 'search.html', context)

def DeleteProduct(request, id) :
    try :
        product = Product.objects.get(id=id)
    except Product.DoesNotExist :
        product = None
    if product == None :
        messages.error(request, "No product found.")
        return redirect('/')
    else :
        if product.seller == request.user :
            product.delete()
            messages.success(request, 'Product deleted successfully.')
        else :
            messages.error(request, "You are not eligible to delete this product.")
        return redirect('/')

# py manage.py runserver
