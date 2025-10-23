from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    # Booking (CRUD)
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('update/<int:id>/', views.update_booking, name='update_booking'),
    path('delete/<int:id>/', views.delete_booking, name='delete_booking'),

    # Payment  (CR)
    path('payment/create/<int:booking_id>/', views.create_payment, name='create_payment'),
    path('my-payments/', views.my_payments, name='my_payments'),

    # Review(CRUD)
    path('review/create/<int:booking_id>/', views.create_review, name='create_review'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('review/update/<int:review_id>/', views.update_review, name='update_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
