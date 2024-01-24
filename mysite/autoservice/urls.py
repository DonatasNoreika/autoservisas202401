from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vehicles/', views.vehicles, name="vehicles"),
    path("vehicles/<int:vehicle_id>", views.vehicle, name="vehicle"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name="search"),
    path('my_orders/', views.MyOrderListView.as_view(), name="my_orders"),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path("order/new", views.OrderCreateView.as_view(), name="order_new"),
]