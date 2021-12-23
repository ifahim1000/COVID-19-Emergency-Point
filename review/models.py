from django.db import models
from product.models import Product
from django.conf import settings

class Review(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        ordering = ("-created_at",)
        
    def __str__(self):
        return str(self.user) + ' , ' + str(self.product) + ' , ' + str(self.comment)