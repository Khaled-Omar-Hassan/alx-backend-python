from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsParticipantOfConversation(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            # If the user is authenticated, check if they are a participant
            return False
        # Instance must have an attribute named `owner`.
        conversation = getattr(obj, 'conversation', obj)
        return request.user in conversation.participants.all()
