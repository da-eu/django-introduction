from django.test import TestCase
from forum.models import Comment, CustomUser
from forum.forms import PostForm

class PostIntegrationTest(TestCase):

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

    def test_get_create_comment_ok(self):
        """GET /forum/post/のリクエスト送信でコメント新規登録ページが表示されることを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        # GET /forum/post/を送信
        response = self.client.get('/forum/post/')

        """結果の検証"""
        # コメント新規登録ページが表示されることを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_create_comment_success(self):
        """POST /forum/post/のリクエスト送信でコメントが新規登録されることを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        data = {        
            'text': 'Yes'
        }

        # POST /forum/post/を送信
        response = self.client.post('/forum/post/', data=data)

        """結果の検証"""
        # リダイレクトされることを検証
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/forum/comments/')

        # コメントが新規登録されていることを検証
        comment = Comment.objects.last()
        self.assertEqual(comment.id, 2)
        self.assertEqual(comment.text, 'Yes')
        self.assertEqual(comment.user, self.user)

    def test_post_create_comment_text_greater_than_max_len(self):
        """textの文字列長が257以上のコメントの新規登録に失敗することを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        data = {        
            'text': 'A' * 257
        }

        # POST /forum/post/を送信
        response = self.client.post('/forum/post/', data=data)

        """結果の検証"""
        # 再度コメント新規登録ページが表示されることを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')

        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        self.assertFormError(form, 'text', 'この値は 256 文字以下でなければなりません( 257 文字になっています)。') # textフィールドにエラーがあることを検証
        self.assertEqual(form.data['text'], 'A' * 257) # 入力値が保持されていることを検証

        # コメントが新規登録されていないことを検証する
        comment = Comment.objects.all()
        self.assertEqual(len(comment), 1)

    def test_post_create_comment_text_less_than_min_len(self):
        """textの文字列長が1未満のコメントの新規登録に失敗することを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        data = {        
            'text': ''
        }

        # POST /forum/post/を送信
        response = self.client.post('/forum/post/', data=data)

        """結果の検証"""
        # 再度コメント新規登録ページが表示されることを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')

        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        self.assertFormError(form, 'text', 'この項目は必須です。') # textフィールドにエラーがあることを検証
        self.assertEqual(form.data['text'], '') # 入力値が保持されていることを検証

        # コメントが新規登録されていないことを検証する
        comment = Comment.objects.all()
        self.assertEqual(len(comment), 1)

    def test_post_create_comment_no_text(self):
        """textの文字列長が257以上のコメントの新規登録に失敗することを確認する"""

        """前提条件"""
        # ログイン実施
        self.client.login(**self.user_credentials)
        
        """手順を実施"""
        data = {}

        # POST /forum/post/を送信
        response = self.client.post('/forum/post/', data=data)

        """結果の検証"""
        # 再度コメント新規登録ページが表示されることを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post.html')

        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        self.assertFormError(form, 'text', 'この項目は必須です。') # textフィールドにエラーがあることを検証

        # コメントが新規登録されていないことを検証する
        comment = Comment.objects.all()
        self.assertEqual(len(comment), 1)