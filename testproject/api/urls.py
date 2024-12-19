from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('comment/', views.CommentAPI.as_view()),
    path('comment/<int:comment_id>/', views.CommentDetailAPI.as_view()),
]