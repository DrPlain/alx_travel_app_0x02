from django.contrib import admin
from .models import User, Review, Property, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Property)
admin.site.register(Booking)
