from django.contrib.auth.mixins import UserPassesTestMixin

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user
