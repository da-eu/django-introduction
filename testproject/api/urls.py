from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('comments/', views.CommentAPI.as_view()),
    path('comments/<int:id>/', views.CommentDetailAPI.as_view()),
]