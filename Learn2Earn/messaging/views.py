from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message, Notification


# MESSAGE CRUD

def inbox(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    #(user je pathaise)
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')

#   (user je paise)
    received_messages = Message.objects.filter(receiver=request.user).order_by('-sent_at')

    return render(request, 'messaging/inbox.html', {
        'sent_messages': sent_messages,
        'received_messages': received_messages
    })
    return render(request, 'messaging/inbox.html', {'messaging': messages})

def send_to_provider(request, provider_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    provider = User.objects.get(id=provider_id)

    if request.method == 'POST':
        content = request.POST['content']

        Message.objects.create(
            sender=request.user,
            receiver=provider,
            content=content
        )

        # Notification create 
        Notification.objects.create(
            receiver=provider,
            message=f"New message from {request.user.username}: {content[:50]}..."
        )

        return redirect('messaging:inbox')

    return render(request, 'messaging/send_message.html', {'provider': provider})

def update_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    message = Message.objects.get(id=message_id)

    if request.method == 'POST':
        message.content = request.POST['content']
        message.save()
        return redirect('messaging:inbox')

    return render(request, 'messaging/update_message.html', {'message': message})


def delete_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    message = Message.objects.get(id=message_id)

    if request.method == 'POST':
        message.delete()
        return redirect('messaging:inbox')

    return render(request, 'messaging/delete_message.html', {'message': message})


# NOTIFICATION

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    notifications_list = Notification.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'messaging/notifications.html', {'notifications_list': notifications_list})

def delete_notification(request, notification_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    notification = Notification.objects.get(id=notification_id)

    if request.method == 'POST':
        notification.delete()
        return redirect('messaging:notifications')

    return render(request, 'messaging/delete_notification.html', {'notification': notification})

