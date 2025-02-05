from django.db import models
from uuid import uuid4


class User(models.Model):
    USER_ROLES = (
        ('host', 'Host'),
        ('guest', 'Guest'),
    )

    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Property(models.Model):
    property_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='properties')  # ForeignKey linking to User
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Review(models.Model):
    Review_id = models.UUIDField(
        default=uuid4, primary_key=True, editable=False)
    property_id = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.property} - Rating: {self.rating}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    )

    booking_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    property_id = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='bookings')
    # Guest who made the booking
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        if self.start_date and self.end_date:
            duration = (self.end_date - self.start_date).days
            if duration > 0:
                if hasattr(self.property_id, 'price_per_night'):
                    total_price = duration * self.property_id.price_per_night
                    return total_price
                else:
                    raise AttributeError(
                        "Property model must have a 'price_per_night' field.")
        return 0

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property} by {self.user}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.status}"