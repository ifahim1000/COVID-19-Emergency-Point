from django.db import models
from account.models import Buyer

class Affiliate(models.Model) :
    user = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    aff_id = models.CharField(max_length=20)
    total_sales = models.IntegerField()
    total_commission = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        ordering = ("-created_at",)
    def __str__(self):
        return str(self.aff_id)
    