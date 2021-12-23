from django.db import models
from django.conf import settings
from product.models import Product
  
class Order(models.Model) :
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=40, decimal_places=2)
    status = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta :
        ordering = ('-date_created',)
    def __str__(self):
        return str(self.user) + ' , ' + str(self.product)