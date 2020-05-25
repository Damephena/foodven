from django.urls import path, include
from .views import (
    MenuListView,
    MenuDetailView,
    OrderListView,
    OrderDetailView,
    CancelOrderView,
    OrderReadyStatusView,
    OrderProgressStatusView,
    ReportListView,
    ReportGenerateView,
    ReportDetailView,
    NotificationListView,
    NotificationDetailView,
)

urlpatterns = [
    path('menus/', MenuListView.as_view(), name="menu-list"),
    path('menus/<str:pk>', MenuDetailView.as_view(), name="menu-detail"),
    path('orders/', OrderListView.as_view(), name="order-list"),
    path('orders/<str:pk>', OrderDetailView.as_view(), name="order-detail"),
    path('orders/<str:pk>/cancel', CancelOrderView.as_view(), name="order-cancel"),
    path('orders/<str:pk>/ready', OrderReadyStatusView.as_view(), name="order-ready"),
    path('orders/<str:pk>/progress', OrderProgressStatusView.as_view(), name="order-progress"),
    path('reports/list', ReportListView.as_view(), name="report-list"),
    path('reports/generate', ReportGenerateView.as_view(), name="report-create"),
    path('reports/<str:pk>', ReportDetailView.as_view(), name="report-detail"),
    path('notifications/', NotificationListView.as_view(), name="notification-list"),
    path('notifications/<str:pk>', NotificationDetailView.as_view(), name="notification-detail"),
]
