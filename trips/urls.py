from django.urls import path
from . import views

urlpatterns = [
    path('publish/', views.publish_trip, name='publish_trip'),
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('cancel/<int:trip_id>/', views.cancel_trip, name='cancel_trip'),
    path('api/update-node/<int:trip_id>/', views.update_current_node, name='update_current_node'),
    path('mark-node/<int:trip_id>/', views.mark_node_passed, name='mark_node_passed'),
]
