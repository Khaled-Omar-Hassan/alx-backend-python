from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from .auth import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet,
                basename='conversations')

convo_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet,
                      basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
    path('token/', TokenObtainPairView, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView, name='token_refresh'),
]
