from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Ендпоінт для реєстрації нового користувача."""
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Ендпоінт для перегляду та оновлення профілю авторизованого користувача."""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Повертає поточного користувача (того, хто надав токен)."""
        return self.request.user