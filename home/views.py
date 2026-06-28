from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Lead, Review, Fleet, Destination


def home(request):
    if request.method == 'POST':
        pickup_location = request.POST.get('pickup_location', '').strip()
        drop_location = request.POST.get('drop_location', '').strip()
        journey_date = request.POST.get('journey_date', '').strip()
        travellers = request.POST.get('travellers', '').strip()
        phone = request.POST.get('phone', '').strip()

        if phone:
            Lead.objects.create(
                name="Quick Booking Guest",
                phone=phone,
                pickup_location=pickup_location,
                drop_location=drop_location,
                journey_date=journey_date if journey_date else None,
                message=f"Required Capacity: {travellers}" if travellers else ""
            )
            messages.success(request, 'Your information has been sent! We will call you soon to confirm your booking.')
        else:
            messages.error(request, 'Please provide a valid mobile number.')
        return redirect('home')

    fleet = Fleet.objects.filter(is_active=True).order_by('order')[:3]
    reviews = Review.objects.filter(is_featured=True).order_by('-created_at')[:4]
    return render(request, 'home/home.html', {
        'fleet': fleet,
        'reviews': reviews,
    })


def fleet(request):
    vehicles = Fleet.objects.filter(is_active=True).order_by('order')
    vehicle_type = request.GET.get('type')
    if vehicle_type and vehicle_type != 'all':
        vehicles = vehicles.filter(name__icontains=vehicle_type)
    return render(request, 'home/fleet.html', {'vehicles': vehicles})


def fleet_detail(request, slug):
    vehicle = Fleet.objects.filter(slug=slug).first()
    template_name = 'home/fleet_detail.html'
    if '14' in slug:
        template_name = 'home/fleet_detail_14.html'
    elif '12' in slug:
        template_name = 'home/fleet_detail_12.html'
    return render(request, template_name, {'slug': slug, 'vehicle': vehicle})


def gallery(request):
    return render(request, 'home/gallery.html')


def about(request):
    return render(request, 'home/about.html')


def destinations(request):
    all_destinations = Destination.objects.order_by('order')
    return render(request, 'home/destinations.html', {
        'destinations': all_destinations,
    })


def reviews(request):
    all_reviews = Review.objects.order_by('-is_featured', '-created_at')
    return render(request, 'home/reviews.html', {'reviews': all_reviews})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('mobile', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        subject = request.POST.get('subject', '').strip()

        if name and phone:
            Lead.objects.create(
                name=name,
                phone=phone,
                email=email or None,
                message=f"Subject: {subject}\n\n{message}" if subject else message,
            )
            messages.success(request, 'Your query has been sent successfully! Our team will get in touch with you shortly.')
        else:
            messages.error(request, 'Please fill in your name and phone number.')
        return redirect('contact')

    return render(request, 'home/contact.html')

def submit_lead_floating(request):
    if request.method == 'POST':
        pickup_city = request.POST.get('pickup_city', '').strip()
        drop_city = request.POST.get('drop_city', '').strip()
        journey_date = request.POST.get('journey_date', '').strip()
        travellers = request.POST.get('travellers', '').strip()
        phone = request.POST.get('phone', '').strip()
        next_url = request.POST.get('next', '/')

        if phone:
            Lead.objects.create(
                name="Quick Booking Guest",
                phone=phone,
                pickup_location=pickup_city,
                drop_location=drop_city,
                journey_date=journey_date if journey_date else None,
                message=f"Submitted via Floating Form. Travellers Capacity: {travellers}"
            )
            messages.success(request, 'Your query is sent successfully! We will contact you shortly.')
        else:
            messages.error(request, 'Please provide your mobile number.')
            
        return redirect(next_url)
    return redirect('home')