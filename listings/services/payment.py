import requests
from alx_travel_app import settings
from ..models import User, Booking, Payment

CHAPA_API_URL = "https://api.chapa.co/v1/transaction"


def initiate_payment(user: User, booking: Booking):
    """Handles payment initialization with Chapa."""
    url = f"{CHAPA_API_URL}/initialize"
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
               "Content-Type": "application/json"}

    # payload = {
    #     "amount": booking.total_price,
    #     "currency": "ETB",
    #     "email": user.email,
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "phone_number": user.phone_number,
    #     "tx_ref": f"booking_{booking.booking_id}",
    #     # "callback_url": "https://yourdomain.com/payment/callback/",
    #     # "return_url": "https://yourdomain.com/payment/success/",
    # }

    payload = {
        "amount": 500,
        "currency": "USD",
        # "email": user.email,
        # "first_name": user.first_name,
        # "last_name": user.last_name,
        "phone_number": '0900123456',
        "tx_ref": f"booking_{booking.booking_id}",
        # "callback_url": "https://yourdomain.com/payment/callback/",
        # "return_url": "https://yourdomain.com/payment/success/",
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if response_data.get("status") == "success":
        # Create Payment record
        payment = Payment.objects.create(
            user=user,
            booking_reference=f"booking_{booking.booking_id}",
            amount=booking.total_price,
            transaction_id=response_data["data"]["tx_ref"],
            status="Pending"
        )
        return {"success": True, "payment_url": response_data["data"]["checkout_url"], "payment": payment}

    return {"success": False, "error": "Payment initiation failed"}


def verify_payment(payment: Payment):
    """Verifies a payment status with Chapa."""
    url = f"{CHAPA_API_URL}/verify/{payment.transaction_id}"
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data.get("status") == "success":
        payment.status = "Completed"
        payment.save()
        return {"success": True, "message": "Payment successful"}

    return {"success": False, "message": "Payment verification failed"}
