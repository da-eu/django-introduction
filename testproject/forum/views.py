from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm, PostForm, LoginForm
from .models import Comment
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

User = get_user_model()

@login_required
def index_view(request):
    return redirect(to='comments')

@login_required
def users_view(request):
    users = User.objects.prefetch_related('comments').order_by('date_joined')

    paginator = Paginator(users, 3)
    number = int(request.GET.get('p', 1))
    page_obj = paginator.page(number)

    context = {
        'page_obj' : page_obj
    }

    return render(request, 'forum/users.html', context)

@login_required
def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    comments = Comment.objects.filter(user=user).order_by('date')

    paginator = Paginator(comments, 3)
    number = int(request.GET.get('p', 1))
    page_obj = paginator.page(number)

    context = {
        'user' : user,
        'page_obj' : page_obj
    }

    return render(request, 'forum/user.html', context)

@login_required
def comments_view(request):
    comments = Comment.objects.select_related('user').order_by('date')

    paginator = Paginator(comments, 3)
    number = int(request.GET.get('p', 1))
    page_obj = paginator.page(number)

    context = {
        'page_obj' : page_obj
    }

    return render(request, 'forum/comments.html', context)

@login_required
def comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    context = {
        'comment' : comment
    }

    return render(request, 'forum/comment.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user', user.id)

    else:
        form = RegisterForm()
    
    context = {
        'form': form
    }

    return render(request, 'forum/register.html', context)

@login_required
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            comment = form.instance
            comment.user = request.user
            comment.save()
            
            return redirect('comments')
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'forum/post.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect('user', user.id)

    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'forum/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')