from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    path('fleet/', views.fleet, name='fleet'),

    path('fleet/<slug:slug>/', views.fleet_detail, name='fleet_detail'),

    path('gallery/', views.gallery, name='gallery'),

    path('about/', views.about, name='about'),

    path('destinations/', views.destinations, name='destinations'),

    path('reviews/', views.reviews, name='reviews'),

    path('contact/', views.contact, name='contact'),

    path('submit-lead-floating/', views.submit_lead_floating, name='submit_lead_floating'),
]