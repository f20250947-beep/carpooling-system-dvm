

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TripForm
from .models import Trip, TripRoute
from .utils import find_route
from rest_framework.decorators import api_view
from rest_framework.response import Response

@login_required
def publish_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = request.user
            route = find_route(trip.start_node, trip.end_node)
            if route is None:
                form.add_error(None, 'No route found between these nodes.')
                return render(request, 'trips/publish_trip.html', {'form': form})
            trip.save()
            for i, node in enumerate(route):
                TripRoute.objects.create(trip=trip, node=node, order=i)
            return redirect('driver_dashboard')
    else:
        form = TripForm()
    return render(request, 'trips/publish_trip.html', {'form': form})

@login_required
def driver_dashboard(request):
    trips = Trip.objects.filter(driver=request.user)
    return render(request, 'trips/driver_dashboard.html', {'trips': trips})
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def cancel_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, driver=request.user)
    if trip.status == 'not_started':
        trip.status = 'cancelled'
        trip.save()
    return redirect('driver_dashboard')


@api_view(['POST'])
def update_current_node(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, driver=request.user)
    node_id = request.data.get('node_id')
    
    try:
        trip_route = TripRoute.objects.get(trip=trip, node_id=node_id)
        trip_route.is_passed = True
        trip_route.save()
        trip.status = 'active'
        trip.save()
        return Response({'success': True})
    except TripRoute.DoesNotExist:
        return Response({'error': 'Node not on route'}, status=400)


@login_required
def mark_node_passed(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, driver=request.user)
    node_id = request.POST.get('node_id')
    try:
        trip_route = TripRoute.objects.get(trip=trip, node_id=node_id)
        trip_route.is_passed = True
        trip_route.save()
        trip.status = 'active'
        trip.save()
    except TripRoute.DoesNotExist:
        pass
    return redirect('driver_dashboard')