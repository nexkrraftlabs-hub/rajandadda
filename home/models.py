from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Lead(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    pickup_location = models.CharField(max_length=300, blank=True, null=True)
    drop_location = models.CharField(max_length=300, blank=True, null=True)
    journey_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Review(models.Model):
    customer_name = models.CharField(max_length=200)
    rating = models.IntegerField(default=5)  # 1 to 5
    content = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.customer_name}"

class Fleet(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    seats = models.CharField(max_length=100)
    fare_per_km = models.CharField(max_length=100)
    driver_charges = models.CharField(max_length=100)
    extra_charges = models.CharField(max_length=300)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='fleet/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

class Destination(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100) # hill, pilgrimage, historical, wildlife, religious
    distance = models.CharField(max_length=100)
    starting_price = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
