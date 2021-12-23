from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import request

class CustomUserManager(BaseUserManager) :
    def create_user(self, email, name, phone, address, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, address, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            address=address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser) :
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Buyer(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    image = models.ImageField(upload_to='buyer/', blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.user
    
    def get_image(self) :
        if self.image :
            return 'http://'+ get_current_site(request).domain + self.image.url
        else :
            return ''

class Provider(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    image = models.ImageField(upload_to='provider/', blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.user
    
    def get_image(self) :
        if self.image :
            return 'http://'+ get_current_site(request).domain + self.image.url
        else :
            return ''