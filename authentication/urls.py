from django.urls import path

from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>/', views.UserDetail.as_view()),
]
