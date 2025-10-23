from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('send/<int:provider_id>/', views.send_to_provider, name='send_to_provider'),
    path('update/<int:message_id>/', views.update_message, name='update_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),  
]
