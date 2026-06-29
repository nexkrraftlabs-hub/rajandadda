from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Fleet

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'fleet', 'gallery', 'contact', 'destinations', 'reviews']

    def location(self, item):
        return reverse(item)

class FleetSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Fleet.objects.filter(is_active=True)

    def location(self, item):
        return reverse('fleet_detail', kwargs={'slug': item.slug})
