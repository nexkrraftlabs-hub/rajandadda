from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from home.models import Lead, Review, Fleet, Destination, AdminProfile


# ─────────────────────────────────────────────
#  Auth
# ─────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ─────────────────────────────────────────────
#  Home / Stats
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def dashboard_home(request):
    now = timezone.now()
    context = {
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(is_read=False).count(),
        'total_reviews': Review.objects.count(),
        'featured_reviews': Review.objects.filter(is_featured=True).count(),
        'total_fleet': Fleet.objects.count(),
        'active_fleet': Fleet.objects.filter(is_active=True).count(),
        'total_destinations': Destination.objects.count(),
        'recent_leads': Lead.objects.order_by('-created_at')[:5],
        'unread_leads_count': Lead.objects.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/home.html', context)


# ─────────────────────────────────────────────
#  Leads
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def leads_list(request):
    leads = Lead.objects.order_by('-created_at')
    # Capture unread IDs before marking as read (for display in template)
    unread_ids = set(Lead.objects.filter(is_read=False).values_list('id', flat=True))
    # Mark all unread leads as read
    Lead.objects.filter(is_read=False).update(is_read=True)
    # Annotate leads with a temporary 'is_new' attribute
    for lead in leads:
        lead.is_new = lead.id in unread_ids
    return render(request, 'dashboard/leads_list.html', {'leads': leads})


@login_required(login_url='dashboard_login')
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Lead deleted successfully.')
    return redirect('leads_list')


# ─────────────────────────────────────────────
#  Reviews
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def reviews_list(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'dashboard/reviews_list.html', {'reviews': reviews})


@login_required(login_url='dashboard_login')
def review_add(request):
    if request.method == 'POST':
        Review.objects.create(
            customer_name=request.POST.get('customer_name'),
            rating=int(request.POST.get('rating', 5)),
            content=request.POST.get('content'),
            is_featured=request.POST.get('is_featured') == 'on',
        )
        messages.success(request, 'Review added successfully.')
        return redirect('reviews_list_dashboard')
    return render(request, 'dashboard/review_form.html', {'action': 'Add'})


@login_required(login_url='dashboard_login')
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.customer_name = request.POST.get('customer_name')
        review.rating = int(request.POST.get('rating', 5))
        review.content = request.POST.get('content')
        review.is_featured = request.POST.get('is_featured') == 'on'
        review.save()
        messages.success(request, 'Review updated successfully.')
        return redirect('reviews_list_dashboard')
    return render(request, 'dashboard/review_form.html', {'action': 'Edit', 'review': review})


@login_required(login_url='dashboard_login')
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
    return redirect('reviews_list_dashboard')


# ─────────────────────────────────────────────
#  Fleet
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def fleet_list(request):
    vehicles = Fleet.objects.order_by('order')
    return render(request, 'dashboard/fleet_list.html', {'vehicles': vehicles})


@login_required(login_url='dashboard_login')
def fleet_add(request):
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        vehicle = Fleet.objects.create(
            name=name,
            slug=slug,
            description=request.POST.get('description', ''),
            seats=request.POST.get('seats', ''),
            fare_per_km=request.POST.get('fare_per_km', ''),
            driver_charges=request.POST.get('driver_charges', ''),
            extra_charges=request.POST.get('extra_charges', ''),
            image_url=request.POST.get('image_url', ''),
            is_active=request.POST.get('is_active') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        if request.FILES.get('image'):
            vehicle.image = request.FILES['image']
            vehicle.image_url = ''
            vehicle.save()
        messages.success(request, 'Vehicle added successfully.')
        return redirect('fleet_list_dashboard')
    return render(request, 'dashboard/fleet_form.html', {'action': 'Add'})


@login_required(login_url='dashboard_login')
def fleet_edit(request, pk):
    vehicle = get_object_or_404(Fleet, pk=pk)
    if request.method == 'POST':
        from django.utils.text import slugify
        vehicle.name = request.POST.get('name')
        vehicle.slug = request.POST.get('slug') or slugify(vehicle.name)
        vehicle.description = request.POST.get('description', '')
        vehicle.seats = request.POST.get('seats', '')
        vehicle.fare_per_km = request.POST.get('fare_per_km', '')
        vehicle.driver_charges = request.POST.get('driver_charges', '')
        vehicle.extra_charges = request.POST.get('extra_charges', '')
        vehicle.is_active = request.POST.get('is_active') == 'on'
        vehicle.order = int(request.POST.get('order', 0))
        if request.FILES.get('image'):
            vehicle.image = request.FILES['image']
            vehicle.image_url = ''
        else:
            vehicle.image_url = request.POST.get('image_url', '')
        vehicle.save()
        messages.success(request, 'Vehicle updated successfully.')
        return redirect('fleet_list_dashboard')
    return render(request, 'dashboard/fleet_form.html', {'action': 'Edit', 'vehicle': vehicle})


@login_required(login_url='dashboard_login')
def fleet_delete(request, pk):
    vehicle = get_object_or_404(Fleet, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted.')
    return redirect('fleet_list_dashboard')


# ─────────────────────────────────────────────
#  Destinations
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def destinations_list(request):
    destinations = Destination.objects.order_by('order')
    return render(request, 'dashboard/destinations_list.html', {'destinations': destinations})


@login_required(login_url='dashboard_login')
def destination_add(request):
    if request.method == 'POST':
        destination = Destination.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category', 'other'),
            distance=request.POST.get('distance', ''),
            starting_price=request.POST.get('starting_price', ''),
            image_url=request.POST.get('image_url', ''),
            is_featured=request.POST.get('is_featured') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        if request.FILES.get('image'):
            destination.image = request.FILES['image']
            destination.image_url = ''
            destination.save()
        messages.success(request, 'Destination added successfully.')
        return redirect('destinations_list_dashboard')
    return render(request, 'dashboard/destination_form.html', {'action': 'Add'})


@login_required(login_url='dashboard_login')
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.name = request.POST.get('name')
        destination.category = request.POST.get('category', 'other')
        destination.distance = request.POST.get('distance', '')
        destination.starting_price = request.POST.get('starting_price', '')
        destination.is_featured = request.POST.get('is_featured') == 'on'
        destination.order = int(request.POST.get('order', 0))
        if request.FILES.get('image'):
            destination.image = request.FILES['image']
            destination.image_url = ''
        else:
            destination.image_url = request.POST.get('image_url', '')
        destination.save()
        messages.success(request, 'Destination updated successfully.')
        return redirect('destinations_list_dashboard')
    return render(request, 'dashboard/destination_form.html', {'action': 'Edit', 'destination': destination})


@login_required(login_url='dashboard_login')
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted.')
    return redirect('destinations_list_dashboard')


# ─────────────────────────────────────────────
#  Profile
# ─────────────────────────────────────────────

@login_required(login_url='dashboard_login')
def profile_edit(request):
    user = request.user
    profile, _ = AdminProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        profile.phone = request.POST.get('phone', profile.phone or '')
        profile.bio = request.POST.get('bio', profile.bio or '')

        # Profile image upload
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()

        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                messages.success(request, 'Password updated. Please log in again.')
                user.save()
                logout(request)
                return redirect('dashboard_login')
            else:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'dashboard/profile.html', {'user': user, 'profile': profile})
        user.save()
        messages.success(request, 'Profile updated successfully.')
    return render(request, 'dashboard/profile.html', {'user': user, 'profile': profile})

