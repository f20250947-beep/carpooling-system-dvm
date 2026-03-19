from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CarpoolRequest, DriverOffer
from .utils import calculate_detour
from trips.models import Trip, TripRoute
from network.models import Node
from accounts.models import Wallet, Transaction

@login_required
def submit_request(request):
    if request.method == 'POST':
        pickup_id = request.POST.get('pickup_node')
        dropoff_id = request.POST.get('dropoff_node')
        pickup_node = get_object_or_404(Node, id=pickup_id)
        dropoff_node = get_object_or_404(Node, id=dropoff_id)
        CarpoolRequest.objects.create(
            passenger=request.user,
            pickup_node=pickup_node,
            dropoff_node=dropoff_node
        )
        return redirect('passenger_dashboard')
    nodes = Node.objects.all()
    return render(request, 'carpool/submit_request.html', {'nodes': nodes})

@login_required
def passenger_dashboard(request):
    requests = CarpoolRequest.objects.filter(passenger=request.user)
    return render(request, 'carpool/passenger_dashboard.html', {'requests': requests})

@login_required
def cancel_request(request, request_id):
    carpool_request = get_object_or_404(CarpoolRequest, id=request_id, passenger=request.user)
    if carpool_request.status == 'pending':
        carpool_request.status = 'cancelled'
        carpool_request.save()
    return redirect('passenger_dashboard')

@login_required
def confirm_offer(request, offer_id):
    offer = get_object_or_404(DriverOffer, id=offer_id, carpool_request__passenger=request.user)
    
    # Check wallet balance
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    if wallet.balance < offer.fare:
        messages.error(request, 'Insufficient wallet balance!')
        return redirect('passenger_dashboard')
    
    # Deduct fare from passenger
    wallet.balance -= offer.fare
    wallet.save()
    Transaction.objects.create(
        user=request.user,
        amount=offer.fare,
        transaction_type='fare_deduct',
        trip=offer.trip
    )
    
    # Add earning to driver
    driver_wallet, created = Wallet.objects.get_or_create(user=offer.driver)
    driver_wallet.balance += offer.fare
    driver_wallet.save()
    Transaction.objects.create(
        user=offer.driver,
        amount=offer.fare,
        transaction_type='earning',
        trip=offer.trip
    )
    
    offer.status = 'accepted'
    offer.save()
    offer.carpool_request.status = 'confirmed'
    offer.carpool_request.save()
    return redirect('passenger_dashboard')

@login_required
def driver_requests(request):
    active_trips = Trip.objects.filter(driver=request.user, status__in=['not_started', 'active'])
    trip_requests = []
    for trip in active_trips:
        remaining = list(trip.route.filter(is_passed=False).values_list('node_id', flat=True))
        nearby_nodes = set()
        for node_id in remaining:
            node = Node.objects.get(id=node_id)
            from trips.utils import find_route
            for other_node in Node.objects.all():
                route = find_route(node, other_node)
                if route and len(route) <= 3:
                    nearby_nodes.add(other_node.id)
        pending_requests = CarpoolRequest.objects.filter(
            status='pending',
            pickup_node_id__in=nearby_nodes,
            dropoff_node_id__in=nearby_nodes
        )
        for req in pending_requests:
            detour, fare = calculate_detour(trip, req.pickup_node, req.dropoff_node)
            trip_requests.append({
                'trip': trip,
                'request': req,
                'detour': detour,
                'fare': fare
            })
    return render(request, 'carpool/driver_requests.html', {'trip_requests': trip_requests})

@login_required
def make_offer(request, request_id):
    carpool_request = get_object_or_404(CarpoolRequest, id=request_id)
    active_trips = Trip.objects.filter(driver=request.user, status__in=['not_started', 'active'])
    if active_trips.exists():
        trip = active_trips.first()
        detour, fare = calculate_detour(trip, carpool_request.pickup_node, carpool_request.dropoff_node)
        if detour is not None:
            DriverOffer.objects.create(
                carpool_request=carpool_request,
                driver=request.user,
                trip=trip,
                detour=detour,
                fare=fare
            )
    return redirect('driver_requests')

