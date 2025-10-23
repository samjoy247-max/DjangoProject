from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import UserProfile, Service
from .forms import ServiceForm
from reservation.models import Review, Booking


def home(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'home.html', {'profile': profile})
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, user_type=user_type)

        return redirect('users:login')

    return render(request, 'users/auth/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'users/auth/login.html')



def logout_user(request):
    logout(request)
    return redirect('home')



def profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'users/profile/profile.html', {'profile': profile})
    return redirect('users:login')



def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        profile.user.username = username
        profile.user.email = email
        profile.user.save()

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        return redirect('users:profile')

    return render(request, 'users/profile/update_profile.html', {'profile': profile})



def delete_user(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

    return render(request, 'users/auth/delete_user.html')



def service_list(request):
    services = Service.objects.all()

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'users/services/service_list.html', {'services': services, 'profile': profile})

    return render(request, 'users/services/service_list.html', {'services': services})


# SERVICE DETAIL
# SERVICE DETAIL
def service_detail(request, service_id):


    service = Service.objects.get(pk=service_id)

    # Get all reviews for this service
    reviews = Review.objects.filter(booking__service=service).order_by('-created_at')

    return render(request, 'users/services/service_detail.html', {
        'service': service,
        'reviews': reviews
    })



def create_service(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    profile = UserProfile.objects.get(user=request.user)

    if profile.user_type != 'provider':
        return render(request, 'users/services/not_provider.html')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('users:service_list')
    else:
        form = ServiceForm()

    return render(request, 'users/services/create_service.html', {'form': form})



def update_service(request, service_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('users:service_detail', service_id=service.id)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'users/services/update_service.html', {'form': form, 'service': service})



def delete_service(request, service_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        service = Service.objects.get(pk=service_id).delete()
        return redirect('users:service_list')

    service = Service.objects.get(pk=service_id)
    return render(request, 'users/services/delete_service.html', {'service': service})



def my_services(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    services = Service.objects.filter(provider=request.user)
    return render(request, 'users/services/my_services.html', {'services': services})
