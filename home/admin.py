from django.contrib import admin
from .models import Lead, Review, Fleet, Destination

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'journey_date', 'created_at')
    search_fields = ('name', 'phone', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_featured')

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('name', 'seats', 'fare_per_km', 'is_active', 'order')
    list_editable = ('order', 'is_active', 'fare_per_km')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'starting_price', 'is_featured', 'order')
    list_editable = ('order', 'is_featured')
    list_filter = ('category', 'is_featured')
