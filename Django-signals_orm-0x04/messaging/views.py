from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('')


def get_user_inbox(user):
    root_messages = Message.objects.filter(receiver=user, parent_message__isnull=True) \
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


def get_threaded_inbox(user):
    root_messages = get_user_inbox(user)
    return [build_message_thread(msg) for msg in root_messages]
