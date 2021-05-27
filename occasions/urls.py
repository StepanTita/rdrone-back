from django.urls import path

from occasions import views

app_name = 'occasions'

urlpatterns = [
    path('', views.OccasionsListCreateView.as_view(), name='occasion_list_create'),
    path('<int:pk>/', views.OccasionsRetrieveView.as_view(), name='occasion_retrieve'),
    path('comments/<int:pk>', views.CommentsCreateListView.as_view(), name='comment_create_list'),
    path('resolutions/<int:pk>', views.ResolutionsResponseView.as_view(), name='resolutions_response'),
    path('resolutions/<str:option>/<int:pk>', views.ResolutionsView.as_view(), name='resolutions_create')
]
