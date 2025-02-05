from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Property, User, Booking, Payment
from .serializers import PropertySerializer, UserSerializer,  BookingSerializer
from services.payment import initiate_payment, verify_payment

# Create your views here.


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListingViewset(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Pass the user to the serializer
        serializer.save(host=self.request.user)


class BookingViewset(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """Creates a booking and initiates payment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(user=request.user)

        # Call payment service
        payment_response = initiate_payment(request.user, booking)

        if payment_response["success"]:
            return Response(
                {
                    "message": "Booking created, please complete payment",
                    "payment_url": payment_response["payment_url"],
                    "booking": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        # Rollback booking if payment fails
        booking.delete()
        return Response({"error": payment_response["error"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def verify_payment(self, request, pk=None):
        """Verifies payment status for a booking."""
        try:
            booking = self.get_object()
            payment = Payment.objects.get(
                booking_reference=f"booking_{booking.id}")
            verification_response = verify_payment(payment)

            if verification_response["success"]:
                send_payment_confirmation_email.delay(
                    payment.user.email, payment.booking_reference)
                return Response({"message": verification_response["message"]}, status=status.HTTP_200_OK)

            return Response({"message": verification_response["message"]}, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
