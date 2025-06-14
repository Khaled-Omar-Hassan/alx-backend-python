from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    objects = UnreadMessagesManager()
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    unread = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID: {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User, related_name='edited_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"
