from django.core.management.base import BaseCommand
from home.models import Fleet, Destination, Review


class Command(BaseCommand):
    help = 'Seed initial fleet, destinations and reviews data'

    def handle(self, *args, **options):
        # ── Fleet ──
        if not Fleet.objects.exists():
            Fleet.objects.create(
                name='12 Seater Luxury',
                slug='12-seater-luxury',
                description='Perfect for family trips and small corporate groups. Fully equipped with premium recliner seats and luxury amenities.',
                seats='12 Passengers + 1 Driver',
                fare_per_km='₹14 - 16 / km',
                driver_charges='₹500 / Day',
                extra_charges='300 KM (Per Day) Extra, All Tax, Parking Extra',
                image_url='https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=800&q=80',
                is_active=True, order=1
            )
            Fleet.objects.create(
                name='14 Seater Premium',
                slug='14-seater-luxury',
                description='Extended legroom and ultra-plush seating for mid-sized groups seeking true comfort on long journeys.',
                seats='14 Passengers + 1 Driver',
                fare_per_km='₹16 - 18 / km',
                driver_charges='₹500 / Day',
                extra_charges='300 KM (Per Day) Extra, All Tax, Parking Extra',
                image_url='https://images.unsplash.com/photo-1570125909232-eb263c188f7e?auto=format&fit=crop&w=800&q=80',
                is_active=True, order=2
            )
            Fleet.objects.create(
                name='20 Seater Maharaja',
                slug='20-seater-maharaja',
                description='The absolute pinnacle of road luxury. Recliner seats, ambient lighting, and immense space for the ultimate journey.',
                seats='20 Passengers + 1 Driver',
                fare_per_km='₹36 - 40 / km',
                driver_charges='₹700 / Day',
                extra_charges='300 KM (Per Day) Extra, All Tax, Parking Extra',
                image_url='https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80',
                is_active=True, order=3
            )
            self.stdout.write(self.style.SUCCESS('✓ Seeded 3 fleet vehicles'))
        else:
            self.stdout.write('  Fleet already has data, skipping.')

        # ── Reviews ──
        if not Review.objects.exists():
            reviews_data = [
                ('Amit Verma', 5, 'Excellent service! The tempo traveller was very clean, luxurious and on time. Driver was professional and polite. Highly recommended for family trips.', True),
                ('Neha Singh', 5, 'We booked for outstation trip to Manali. The vehicle was in perfect condition with all luxury amenities. Our journey was so comfortable.', True),
                ('Rohit Sharma', 5, 'Best tempo traveller service in Lucknow. No hidden charges and very transparent pricing. Will surely book again.', True),
                ('Pankaj Tiwari', 5, 'Very good experience with Rajan Dadda Tours & Travellers. Clean vehicle, good music system and cooperative driver.', True),
                ('Sunita Agarwal', 5, 'Amazing experience! Booked 14 seater for family pilgrimage. Driver was knowledgeable and very helpful throughout the journey.', False),
                ('Deepak Gupta', 5, 'Professional service from start to finish. The vehicle was well maintained and the driver was punctual. Highly recommended!', False),
            ]
            for name, rating, content, featured in reviews_data:
                Review.objects.create(
                    customer_name=name, rating=rating,
                    content=content, is_featured=featured
                )
            self.stdout.write(self.style.SUCCESS('✓ Seeded 6 reviews'))
        else:
            self.stdout.write('  Reviews already has data, skipping.')

        # ── Destinations ──
        if not Destination.objects.exists():
            destinations_data = [
                ('Manali', 'hill', '570 km', '₹18,000', 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80', True, 1),
                ('Nainital', 'hill', '340 km', '₹12,000', 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=80', True, 2),
                ('Varanasi', 'pilgrimage', '300 km', '₹10,000', 'https://images.unsplash.com/photo-1561361058-c24cecae35ca?auto=format&fit=crop&w=800&q=80', True, 3),
                ('Agra', 'historical', '360 km', '₹11,000', 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80', True, 4),
                ('Mathura Vrindavan', 'religious', '460 km', '₹14,000', 'https://images.unsplash.com/photo-1590077428593-a55bb07c4665?auto=format&fit=crop&w=800&q=80', False, 5),
                ('Jim Corbett', 'wildlife', '410 km', '₹13,000', 'https://images.unsplash.com/photo-1518992096823-a58fb51f1a5c?auto=format&fit=crop&w=800&q=80', False, 6),
                ('Haridwar & Rishikesh', 'pilgrimage', '380 km', '₹12,500', 'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?auto=format&fit=crop&w=800&q=80', False, 7),
                ('Shimla', 'hill', '620 km', '₹20,000', 'https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=800&q=80', False, 8),
            ]
            for name, category, distance, price, image, featured, order in destinations_data:
                Destination.objects.create(
                    name=name, category=category, distance=distance,
                    starting_price=price, image_url=image,
                    is_featured=featured, order=order
                )
            self.stdout.write(self.style.SUCCESS('✓ Seeded 8 destinations'))
        else:
            self.stdout.write('  Destinations already has data, skipping.')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete! Your site now has dynamic content.'))
