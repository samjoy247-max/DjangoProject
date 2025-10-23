from django.shortcuts import render, redirect
from .models import Booking, Payment, Review
from .forms import ReviewForm
from users.models import Service


# BOOKING CRUD 

def create_booking(request, service_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        booking_date = request.POST['booking_date']
        duration = int(request.POST['duration'])
        total_amount = service.price_per_hour * duration

        Booking.objects.create(
            provider=service.provider,
            seeker=request.user,
            service=service,
            booking_date=booking_date,
            duration=duration,
            total_amount=total_amount
        )

        return redirect('reservation:my_bookings')

    return render(request, 'reservation/booking_create.html', {'service': service})


def my_bookings(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    bookings = Booking.objects.filter(seeker=request.user) | Booking.objects.filter(provider=request.user)
    bookings = bookings.order_by('-created_at')
    return render(request, 'reservation/booking_list.html', {'bookings': bookings})


def update_booking(request, id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    booking = Booking.objects.get(id=id)

    if request.method == 'POST':
        booking.booking_date = request.POST['booking_date']
        booking.duration = int(request.POST['duration'])
        booking.total_amount = booking.service.price_per_hour * booking.duration
        booking.save()
        return redirect('reservation:my_bookings')

    return render(request, 'reservation/booking_update.html', {'booking': booking})


def delete_booking(request, id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    booking = Booking.objects.get(id=id)

    if request.method == 'POST':
        booking.delete()
        return redirect('reservation:my_bookings')

    return render(request, 'reservation/booking_delete.html', {'booking': booking})


# PAYMENT - Only CR 

def create_payment(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']

        Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            transaction_id=transaction_id
        )

        
        booking.status = 'completed'
        booking.save()

        return redirect('reservation:my_bookings')

    return render(request, 'reservation/payment_create.html', {'booking': booking})


def my_payments(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    payments = Payment.objects.filter(booking__seeker=request.user) | Payment.objects.filter(
        booking__provider=request.user)
    payments = payments.order_by('-payment_date')
    return render(request, 'reservation/payment_list.html', {'payments': payments})


# REVIEW CRUD


def create_review(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']

        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )

        return redirect('reservation:my_bookings')

    return render(request, 'reservation/review_create.html', {'booking': booking})


def my_reviews(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    reviews = Review.objects.filter(booking__seeker=request.user).order_by('-created_at')
    return render(request, 'reservation/review_list.html', {'reviews': reviews})


def update_review(request, review_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return redirect('reservation:my_reviews')

    return render(request, 'reservation/review_update.html', {'review': review})


def delete_review(request, review_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.delete()
        return redirect('reservation:my_reviews')

    return render(request, 'reservation/review_delete.html', {'review': review})
