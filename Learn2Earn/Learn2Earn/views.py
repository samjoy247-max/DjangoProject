from django.shortcuts import render
from users.models import UserProfile

def home(request):
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()

    return render(request, 'home.html', {'profile': profile})
