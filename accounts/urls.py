from django.urls import path
from . import views
from carpool.views import passenger_dashboard

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('passenger/dashboard/', passenger_dashboard, name='passenger_dashboard'),
    
    path('wallet/topup/', views.topup_wallet, name='topup_wallet'),
    path('choose-role/', views.choose_role, name='choose_role')
]