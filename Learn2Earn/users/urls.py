from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('delete/', views.delete_user, name='delete_user'),

    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/update/', views.update_service, name='update_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    path('my-services/', views.my_services, name='my_services'),
]
