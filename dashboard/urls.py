from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),

    # Home
    path('', views.dashboard_home, name='dashboard_home'),

    # Leads
    path('leads/', views.leads_list, name='leads_list'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),

    # Reviews
    path('reviews/', views.reviews_list, name='reviews_list_dashboard'),
    path('reviews/add/', views.review_add, name='review_add'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # Fleet
    path('fleet/', views.fleet_list, name='fleet_list_dashboard'),
    path('fleet/add/', views.fleet_add, name='fleet_add'),
    path('fleet/<int:pk>/edit/', views.fleet_edit, name='fleet_edit'),
    path('fleet/<int:pk>/delete/', views.fleet_delete, name='fleet_delete'),

    # Destinations
    path('destinations/', views.destinations_list, name='destinations_list_dashboard'),
    path('destinations/add/', views.destination_add, name='destination_add'),
    path('destinations/<int:pk>/edit/', views.destination_edit, name='destination_edit'),
    path('destinations/<int:pk>/delete/', views.destination_delete, name='destination_delete'),

    # Profile
    path('profile/', views.profile_edit, name='profile_edit'),
]
