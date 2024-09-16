from django.http import Http404
from django.shortcuts import redirect, render
from .forms import RegisterForm, PostForm

class User:
    def __init__(self, id, username, email, age):
        self.id = id
        self.username = username
        self.email = email
        self.age = age

import datetime
class Comment:
    def __init__(self, id, text, date):
        self.id = id
        self.text = text
        self.date = date

users = [
    User(1, 'Yamada Taro', 'taro@yamada.jp', 18),
    User(2, 'Yamada Hanako', 'hanako@yamada.jp', 22),
    User(3, 'Sato Saburo', 'saburo@sato.jp', 53),
    User(4, 'Takahashi Shiro', 'shiro@takahashi.jp', 64)
]

comments = [
    Comment(1, 'おはようございます', datetime.datetime(2023, 3, 4, 12, 4, 0)),
    Comment(2, 'いい天気ですねー', datetime.datetime(2023, 4, 5, 16, 21, 0)),
    Comment(3, '明日もよろしくお願いします', datetime.datetime(2000, 12, 25, 1, 55, 0)),
    Comment(4, 'おやすみなさい', datetime.datetime(2024, 1, 1, 1, 37, 0)),
    Comment(5, '山路を登りながら、こう考えた。智に働けば角が立つ。情に棹させば流される。意地を通とおせば窮屈だ。とかくに人の世は住みにくい。', datetime.datetime(2012, 10, 8, 3, 49, 0)),
]

def index_view(request):
    return redirect(to='comments')

def users_view(request):
    context = {
        'users' : users
    }

    return render(request, 'forum/users.html', context)

def user_view(request, user_id):
    if user_id > len(users) or user_id < 1:
        raise Http404('Not found user')

    user = users[user_id - 1]

    context = {
        'user' : user
    }

    return render(request, 'forum/user.html', context)

def comments_view(request):
    context = {
        'comments' : comments
    }

    return render(request, 'forum/comments.html', context)

def comment_view(request, comment_id):
    if comment_id > len(comments) and comment_id < 1:
        raise Http404('Not found comment')

    comment = comments[comment_id - 1]

    context = {
        'comment' : comment
    }

    return render(request, 'forum/comment.html', context)

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            id = len(users) + 1
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            age = form.cleaned_data.get('age')
            
            user = User(id=id, username=username, email=email, age=age)
            users.append(user)

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
            id = len(comments) + 1
            text = form.cleaned_data.get('text')
            date = datetime.datetime.now()   

            comment = Comment(id, text, date)
            comments.append(comment)

            return redirect('comments')
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'forum/post.html', context)