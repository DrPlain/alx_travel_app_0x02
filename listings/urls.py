from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewset, BookingViewset, UserListCreateAPIView


router = DefaultRouter()
router.register('listings', ListingViewset)
router.register('bookings', BookingViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserListCreateAPIView.as_view(), name='user')
]
