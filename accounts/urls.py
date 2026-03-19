from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('passenger/dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    
    path('wallet/topup/', views.topup_wallet, name='topup_wallet'),
]