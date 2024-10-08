from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('comments/', views.CommentList.as_view(), name='comments'),
    path('comment/<int:comment_id>', views.CommentDetail.as_view(), name='comment'),
    path('users/', views.UserList.as_view(), name='users'),
    path('user/<int:user_id>', views.UserDetail.as_view(), name='user'),
    path('register/', views.Register.as_view(), name='register'),
    path('post/', views.Post.as_view(), name='post'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]