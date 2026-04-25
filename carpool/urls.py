from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.submit_request, name='submit_request'),
    path('dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),
    path('confirm/<int:offer_id>/', views.confirm_offer, name='confirm_offer'),
    path('driver/requests/', views.driver_requests, name='driver_requests'),
    path('offer/<int:request_id>/', views.make_offer, name='make_offer'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    
]