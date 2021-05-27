from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
