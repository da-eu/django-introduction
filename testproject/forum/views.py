from .forms import RegisterForm, PostForm, LoginForm
from .models import Comment
from .mixins import AuthorRequiredMixin
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

User = get_user_model()

class Login(LoginView):
    form_class = LoginForm
    template_name = 'forum/login.html'

    def get_success_url(self):
        return reverse('user', kwargs={'user_id':self.request.user.id})

class Logout(LogoutView):
    next_page = reverse_lazy('login')

class Index(RedirectView):
    url = reverse_lazy('comments')

class UserList(LoginRequiredMixin, ListView):
    queryset = User.objects.prefetch_related('comments').order_by('date_joined')
    template_name = 'forum/users.html'
    paginate_by = 3
    page_kwarg = 'p'

class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
    template_name = 'forum/user.html'

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(user=self.object).order_by('date')

        paginator = Paginator(comments, 3)
        number = int(self.request.GET.get('p', 1))
        page_obj = paginator.page(number)

        return super().get_context_data(page_obj=page_obj)


class CommentList(LoginRequiredMixin, ListView):
    queryset = Comment.objects.select_related('user').order_by('date')
    paginate_by = 3
    page_kwarg = 'p'
    template_name = 'forum/comments.html'


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'forum/comment.html'

class Register(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'forum/register.html'

    def form_valid(self, form):
        
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response
    
    def get_success_url(self):
        return reverse('user', kwargs={'user_id':self.object.pk})

class Post(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'forum/post.html'
    success_url = reverse_lazy('comments')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CommentUpdate(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = PostForm
    pk_url_kwarg = 'comment_id'
    template_name = 'forum/update.html'
    success_url = reverse_lazy('comments')

class CommentDelete(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'forum/delete.html'
    success_url = reverse_lazy('comments')