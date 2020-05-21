from django.urls import path, include
from .views import (
    # CustomerView,
    CustomerProfileView,
    CustomerListView, 
    CustomerRegisterView,
    CustomerSetPasswordView,
    LoginView,
    LogoutView,
    # VendorView,
    VendorProfileView,
    VendorListView,
    VendorRegisterView,
    VendorSetPasswordView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('customers/register/', CustomerRegisterView.as_view(), name="customer-register"),
    path('customers/set-password/<str:pk>/', CustomerSetPasswordView.as_view(), name="customer-setpassword"),
    path('vendors/register/', VendorRegisterView.as_view(), name="vendor-register"),
    path('vendors/set-password/<str:pk>/', VendorSetPasswordView.as_view(), name="vendor-setpassword"),
    path('customer/profile/', CustomerProfileView.as_view(), name="customer-profile"),
    path('vendor/profile/', VendorProfileView.as_view(), name="vendor-profile"),
    path('customers/', CustomerListView.as_view(), name="customer-list"),
    path('vendors/', VendorListView.as_view(), name="vendor-list")
]
