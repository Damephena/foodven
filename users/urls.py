from django.urls import path, include
from .views import (
    # CustomerView, 
    CustomerRegisterView,
    CustomerSetPasswordView,
    LoginView,
    # VendorView,
    VendorRegisterView,
    VendorSetPasswordView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('customers/register/', CustomerRegisterView.as_view(), name="customer-register"),
    path('customers/set-password/<str:pk>/', CustomerSetPasswordView.as_view(), name="customer-setpassword"),
    path('vendors/register/', VendorRegisterView.as_view(), name="vendor-register"),
    path('vendors/set-password/<str:pk>/', VendorSetPasswordView.as_view(), name="vendor-setpassword"),
    # path('customers/login/', include('rest_framework.urls'),),
    # path('customers/login/', CustomerLoginView.as_view(), name="customer-login"),
    # path('customers/', CustomerView.as_view(), base_name="customer-view"),
    # path('vendors/', VendorView.as_view(), base_name="vendor-view")
]
