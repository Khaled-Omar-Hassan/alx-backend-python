from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from django.db import models


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('')


def get_user_inbox(request):
    root_messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True, sender=request.user) \
        .select_related('sender') \
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related(
                'sender', 'receiver'))
    )
    return root_messages


def build_message_thread(message):
    """
    Recursively builds a message thread tree.
    """
    thread = {
        'message': message,
        'replies': []
    }
    replies = message.replies.select_related('sender', 'receiver').all()
    for reply in replies:
        thread['replies'].append(build_message_thread(reply))
    return thread


def get_threaded_inbox(request):
    root_messages = get_user_inbox(request.useruser)
    return [build_message_thread(msg) for msg in root_messages]


def unread_inbox(request):
    user = request.user
    unread_msgs = Message.unread.unread_for_user(user).select_related('sender').only(
        'id', 'content', 'timestamp', 'sender__username'
    )
    return render(request, 'messaging/inbox.html', {'messages': unread_msgs})


@cache_page(60)  # Cache timeout set to 60 seconds
def conversation_view(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=other_user) |
         models.Q(sender=other_user, receiver=request.user)),
        parent_message__isnull=True
    ).select_related('sender', 'receiver').order_by('timestamp')

    return render(request, 'messaging/conversation.html', {'messages': messages, 'other_user': other_user})
