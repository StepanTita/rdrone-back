from django.urls import path

from authentication import views
from rest_framework.authtoken import views as rest_views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.UserCreateUpdateView.as_view(), name='auth_register'),
    path('api-token-auth/', rest_views.obtain_auth_token, name='auth_obtain_token'),
    path('<str:username>/', views.UserDetail.as_view(), name='auth_user'),
]
