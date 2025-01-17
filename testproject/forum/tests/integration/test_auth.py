from django.test import TestCase, Client
from forum.models import Comment, CustomUser


class AuthIntegrationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """各テストケースで共通で必要となる変数の準備"""
        super().setUpClass()

        cls.login_url = '/forum/login/'
        cls.user_credentials = {
            'username': 'Hanako',
            'password': 'ppaassss'
        }
        
    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるデータの準備"""

        # ユーザーの作成
        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassss',
            age = 20,
            email='hanako@example.com'
        )

        # コメントの作成
        Comment.objects.create(
            user=cls.user,
            text='Hello'
        )

    def test_forum_comments_access_ok(self):
        """ログインしている場合に/forum/comments/に正常にアクセスできることを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        # /forum/comments/にアクセス
        response = self.client.get('/forum/comments/')

        """結果の検証"""
        # リダイレクトされていないことを検証
        self.assertEqual(response.status_code, 200)

        # ユーザーがログイン中状態になっていることを検証
        self.assertTrue(response.context['user'].is_authenticated)

        # コメント一覧ページに表示されるべき情報がボディに含まれていることを検証
        self.assertContains(response, 'Hanako')
        self.assertContains(response, 'Hello')

    def test_redirect_if_not_logged_in(self):
        """ログインしていない場合に/forum/comments/にアクセス不可であることを確認する""" 

        """手順を実施"""
        # /forum/comments/にアクセス
        response = self.client.get('/forum/comments/')

        """結果の検証"""
        # ログインページにリダイレクトされていることを検証
        self.assertRedirects(response, '/forum/login/?next=/forum/comments/')

    def test_redirect_if_logged_out(self):
        """ログアウト後に/forum/comments/にアクセス不可であることを確認する""" 

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
       
        # /forum/comments/にアクセス
        self.client.get('/forum/comments/')

        """手順を実施"""
        # ログアウト実施
        self.client.logout()

        # /forum/comments/にアクセス
        response = self.client.get('/forum/comments/')

        """結果の検証"""
        # ログインページにリダイレクトされていることを検証
        self.assertRedirects(response, '/forum/login/?next=/forum/comments/')