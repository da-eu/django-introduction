from django.test import TestCase
from django.urls import resolve, reverse
from forum import views

class UrlsTest(TestCase):
    
    def test_url_forum_login_resolve_to_view(self):
        """/forum/login/のURLがLoginにマッピングされていることを確認する"""

        """手順の実施"""
        # URLを解決
        found = resolve('/forum/login/')

        """結果の検証"""
        # マッピングされているビューがLoginであることを検証
        self.assertEqual(found.func.view_class, views.Login)

    def test_name_login_reverse_to_url(self):
        """loginという名前から/forum/login/のURLが逆引きされることを確認する"""

        """手順の実施"""
        # URLを逆引き
        url = reverse('login')

        """結果の検証"""
        # loginという名前から/forum/login/が逆引きされることを検証
        self.assertEqual(url, '/forum/login/')

    def test_url_forum_register_resolve_to_view(self):
        """/forum/register/のURLがRegisterにマッピングされていることを確認する"""

        """手順の実施"""
        # URLを解決
        found = resolve('/forum/register/')

        """結果の検証"""
        # マッピングされているビューがRegisterであることを検証
        self.assertEqual(found.func.view_class, views.Register)

    def test_name_register_reverse_to_url(self):
        """registerという名前から/forum/register/のURLが逆引きされることを確認する"""

        """手順の実施"""
        # URLを逆引き
        url = reverse('register')

        """結果の検証"""
        # registerという名前から/forum/register/が逆引きされることを検証
        self.assertEqual(url, '/forum/register/')