from django.db import models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import request

class Product(models.Model) :
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    stock = models.BooleanField(default=True,)
    image = models.ImageField(upload_to='product/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        ordering = ("-created_at",)
    
    def __str__(self) :
        return self.name
    
    def get_image(self) :
        if self.image :
            return 'http://'+ get_current_site(request).domain + self.image.url
        else :
            return ''