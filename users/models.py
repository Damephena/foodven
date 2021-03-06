from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
# Create your models here.

class Auth(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=500, blank=False, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('auth')
        verbose_name_plural = _('auths')

    def __str__(self):
        return self.first_name


class Vendor(Auth):
    business_name = models.CharField(max_length=250)
    phone_number = PhoneNumberField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.business_name


class Customer(Auth):
    phone_number = PhoneNumberField(blank=True, null=True)
    amount_outstanding = models.FloatField(default=0.00)
    
    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.first_name + " - " + self.last_name

