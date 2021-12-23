from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage, name="homepage"),
    path('add-product', views.AddProduct, name="add_product"),
    path('medicine', views.MedicineProduct ,name="medicine_product"),
    path('icu', views.IcuProduct ,name="icu_product"),
    path('hospital', views.HospitalProduct ,name="hospital_product"),
    path('oxygen', views.OxygenProduct ,name="oxygen_product"),
    path('ambulance', views.AmbulanceProduct ,name="ambulance_product"),
    path('details/<str:id>', views.ProductDetails ,name="product_details"),
    path('delete/<str:id>', views.DeleteProduct ,name="product_delete"),
    path('search', views.SearchProducts, name='search_product'),
] 
