from django.http import HttpResponse, Http404
from django.shortcuts import redirect

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
    return redirect('comments')

def users_view(request):
    body = ''
    
    for user in users:
        body += '<a href="/forum/user/{id}/">{name}</a>'.format(id=user.id,name=user.username)
        body += '\n<br>'

    return HttpResponse(body)

def user_view(request, user_id):
    if user_id > len(users) or user_id < 1:
        raise Http404('Not found user')

    body = ''
    user = users[user_id - 1]

    body += user.username
    body += ','
    body += user.email
    body += ','
    body += str(user.age)
    body += '\n<br>'

    return HttpResponse(body)

def comments_view(request):
    body = ''
    
    for comment in comments:
        body += '<a href="/forum/comment/{id}/">{text}</a>'.format(id=comment.id,text=comment.text)
        body += '\n<br>'

    return HttpResponse(body)

def comment_view(request, comment_id):
    if comment_id > len(comments) or comment_id < 1:
        raise Http404('Not found comment')

    body = ''
    comment = comments[comment_id - 1]

    body += comment.text
    body += ','
    body += '{0:%Y年%m月%d日}'.format(comment.date)
    body += '\n<br>'

    return HttpResponse(body)