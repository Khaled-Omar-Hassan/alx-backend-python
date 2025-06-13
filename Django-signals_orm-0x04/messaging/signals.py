from .models import Message, MessageHistory, Notification
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def track_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    messages = Message.objects.filter(
        sender=instance) | Message.objects.filter(receiver=instance)
    for msg in messages:
        MessageHistory.objects.filter(message=msg).delete()
        Notification.objects.filter(message=msg).delete()
        msg.delete()

    Notification.objects.filter(user=instance).delete()
