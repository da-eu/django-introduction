from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('comments/', views.comments_view, name='comments'),
    path('comment/<int:comment_id>/', views.comment_view, name='comment'),
    path('users/', views.users_view, name='users'),
    path('user/<int:user_id>/', views.user_view, name='user'),
    path('register/', views.register_view, name='register'),
    path('post/', views.post_view, name='post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]