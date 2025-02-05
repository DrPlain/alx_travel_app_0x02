from listings.models import User, Review, Property, Booking
import os
import sys
import django
from datetime import date, timedelta
from random import randint, choice

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app_0x00.settings')
django.setup()


# Seed Users

def seed_users():
    if not User.objects.exists():
        users = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "host1@example.com",
                "password_hash": "hashed_password_1",
                "phone_number": "1234567890",
                "role": "host",
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "host2@example.com",
                "password_hash": "hashed_password_2",
                "phone_number": "0987654321",
                "role": "host",
            },
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "guest1@example.com",
                "password_hash": "hashed_password_3",
                "phone_number": "1231231234",
                "role": "guest",
            },
            {
                "first_name": "Bob",
                "last_name": "Brown",
                "email": "guest2@example.com",
                "password_hash": "hashed_password_4",
                "phone_number": "3213214321",
                "role": "guest",
            },
        ]
        for user_data in users:
            User.objects.create(**user_data)
    print("Users seeded.")

# Seed Properties


def seed_properties():
    if not Property.objects.exists():
        hosts = User.objects.filter(role="host")
        properties = [
            {
                "name": "Luxury Villa",
                "description": "A beautiful villa with amazing views.",
                "price_per_night": 200,
                "host": choice(hosts),
                "location": "New York",
            },
            {
                "name": "Cozy Apartment",
                "description": "A small, cozy apartment for a short stay.",
                "price_per_night": 100,
                "host": choice(hosts),
                "location": "San Francisco",
            },
        ]
        for prop in properties:
            Property.objects.create(**prop)
    print("Properties seeded.")

# Seed Bookings


def seed_bookings():
    if not Booking.objects.exists():
        guests = User.objects.filter(role="guest")
        properties = Property.objects.all()
        for guest in guests:
            for prop in properties:
                Booking.objects.create(
                    user=guest,
                    property=prop,
                    start_date=date.today() + timedelta(days=randint(1, 10)),
                    end_date=date.today() + timedelta(days=randint(11, 20)),
                )
    print("Bookings seeded.")

# Seed Reviews


def seed_reviews():
    if not Review.objects.exists():
        users = User.objects.all()
        properties = Property.objects.all()
        for user in users:
            for prop in properties:
                Review.objects.create(
                    user=user,
                    property=prop,
                    rating=randint(1, 5),
                    comment="Nice place!" if randint(0, 1) else None,
                )
    print("Reviews seeded.")

# Run Seeds


def run_seeds():
    seed_users()
    seed_properties()
    seed_bookings()
    seed_reviews()
    print("Seeding completed!")


if __name__ == "__main__":
    run_seeds()
