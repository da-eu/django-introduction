from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm, PostForm
from .models import User, Comment

def index_view(request):
    return redirect(to='comments')

def users_view(request):
    users = User.objects.all()

    context = {
        'users' : users
    }

    return render(request, 'forum/users.html', context)

def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    context = {
        'user' : user
    }

    return render(request, 'forum/user.html', context)

def comments_view(request):
    comments = Comment.objects.all()

    context = {
        'comments' : comments
    }

    return render(request, 'forum/comments.html', context)

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

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            age = form.cleaned_data.get('age')
            
            user = User(username=username, email=email, age=age)
            user.save()

            return redirect('users')

    else:
        form = RegisterForm()
    
    context = {
        'form': form
    }

    return render(request, 'forum/register.html', context)

def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data.get('text')

            comment = Comment(text=text)
            comment.save()

            return redirect('comments')
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'forum/post.html', context)