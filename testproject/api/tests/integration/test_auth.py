from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from forum.models import Comment, CustomUser


class AuthIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """各テストケースで共通で必要となる準備"""
        super().setUpClass()

        cls.login_url = '/api/token/'

        cls.user_credentials = {
            'username': 'Hanako',
            'password': 'ppaassss'
        }
        
    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるレコードの準備"""

        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassss',
            age = 20,
            email='hanako@example.com'
        )

        Comment.objects.create(
            user=cls.user,
            text='Hello'
        )

        Comment.objects.create(
            user=cls.user,
            text='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )

        token_record = Token.objects.create(user=cls.user)
        cls.token = token_record.key

    def setUp(self):
        """各テストケースで毎回で必要となる初期化"""

        # APIClientのインスタンス生成
        self.client = APIClient()


    def test_get_api_comments_success(self):
        """正しいトークンが送信された場合にGET /api/comments/の実行に成功することを確認する"""

        """前提条件"""
        # トークンの記録
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        """手順を実施"""
        # GET /api/comments/を実行（記録したトークンも送信される）
        response = self.client.get('/api/comments/')
        
        """結果の検証"""
        # レスポンスのステータスコードが200であることを検証
        self.assertEqual(response.status_code, 200)

        # 全レコードが取得できていることを検証
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'Hello')
        self.assertEqual(response.data[0]['user'], 1)
        self.assertEqual(response.data[1]['text'], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.assertEqual(response.data[1]['user'], 1)

    def test_post_api_comments_success(self):
        """正しいトークンが送信された場合にPOST /api/comments/の実行に成功することを確認する"""

        """前提条件"""
        # トークンの記録
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        """手順を実施"""

        data = {
            'text': 'New Comment'
        }

        # POST /api/comments/を実行（記録したトークンも送信される）
        response = self.client.post('/api/comments/', format='json', data=data)
        
        """結果の検証"""
        # レスポンスのステータスコードが201であることを検証
        self.assertEqual(response.status_code, 201)
        
        # 送信したフィールドに応じたレスポンスが返却されていることを検証
        self.assertEqual(response.data['text'], 'New Comment')
        self.assertEqual(response.data['user'], 1)

        # レコードの件数が１件増えていることを検証
        self.assertEqual(len(Comment.objects.all()), 3)

        # 送信したフィールドに応じたレコードがDBに保存されていることを検証
        comment = Comment.objects.get(id=3)
        self.assertEqual(comment.text, 'New Comment')
        self.assertEqual(comment.user, self.user)

    def test_get_api_comments_no_token(self):
        """トークンが送信されない場合にGET /api/comments/の実行に失敗することを確認する"""

        """手順を実施"""
        # GET /api/comments/を実行（トークン無し）
        response = self.client.get('/api/comments/', format='json')
        
        """結果の検証"""
        # レスポンスのステータスコードが201であることを検証
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '認証情報が含まれていません。')

    def test_get_api_comments_invalid_token(self):
        """不正なトークンを送信した場合にGET /api/comments/の実行に失敗することを確認する"""

        """前提条件"""
        # トークンの記録
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')

        """手順を実施"""
        # GET /api/comments/を実行（不正なトークン）
        response = self.client.get('/api/comments/', format='json')
        
        """結果の検証"""
        # レスポンスのステータスコードが201であることを検証
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '不正なトークンです。')