from unittest.mock import MagicMock, patch
from django.test import TestCase, RequestFactory
from django.core.paginator import EmptyPage
from forum.models import CustomUser
from forum.views import Post, Login, UserDetail
from forum.forms import PostForm


class PostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
            email='hanako@example.com'
        )


    def setUp(self):
        self.factory = RequestFactory()

    def test_form_valid_success(self):
        """form_validでリクエスト送信者がコメントの投稿者に設定されることを確認"""

        """前提条件"""

        # 事前にフォームのis_validを成功させておく
        data = {
            'text': 'Yes'
        }

        form = PostForm(data)
        form.is_valid()

        """手順の実施"""

        view = Post()
        
        # リクエストを生成
        request = self.factory.post('/forum/post/', data)
        request.user = self.user
        view.request = request

        # スーパークラスのform_validにモックを仕掛けた状態でform_validを実行
        with patch('django.views.generic.CreateView.form_valid') as mock:
            mock.return_value = None
            view.form_valid(form)

        """結果の検証"""
        # リクエスト送信者がコメントの投稿者に設定されていることを検証
        self.assertIs(form.instance.user, self.user)

class LoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
            email='hanako@example.com'
        )
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_success_url_success(self):
        """get_success_urlでリクエスト送信者のIDがリダイレクト先のURLにセットされることを確認"""

        """手順の実施"""

        view = Login()
        
        # リクエストを生成
        request = self.factory.post('/forum/login/')
        request.user = self.user # ID1のユーザー  
        view.request = request

        url = view.get_success_url()

        """結果の検証"""
        # URLが正しく生成されていることを検証
        self.assertEqual(url, '/forum/user/1')

class UserDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
            email='hanako@example.com'
        )

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_context_data_page_1(self):
        """get_context_dataでページネーション結果のページ1がコンテキストにセットされることを確認"""

        """手順の実施"""

        view = UserDetail()
        view.object = self.user
        
        # リクエストを生成
        request = self.factory.get('/forum/comments/?p=1')
        request.user = self.user
        view.request = request

        # ５件分のレコードのモックを返却するモックのメソッドを作成
        mock_comments = [MagicMock() for _ in range(5)]
        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = mock_comments

        # filterメソッドにモックを仕掛けた状態でget_context_dataを実行
        with patch('forum.models.Comment.objects.filter') as mock:
            mock.return_value = mock_queryset
            context = view.get_context_data()

        """結果の検証"""
        # contextにページネーション結果がセットされていることを検証
        self.assertIn('page_obj', context)
        self.assertEqual(context['page_obj'].object_list, mock_comments[:3])

    def test_get_context_data_page_2(self):
        """get_context_dataでページネーション結果のページ2がコンテキストにセットされることを確認"""

        """手順の実施"""

        view = UserDetail()
        view.object = self.user
        
        # リクエストを生成
        request = self.factory.get('/forum/comments/?p=2')
        request.user = self.user
        view.request = request

        # ５件分のレコードのモックを返却するモックのメソッドを作成
        mock_comments = [MagicMock() for _ in range(5)]
        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = mock_comments

        # filterメソッドにモックを仕掛けた状態でget_context_dataを実行
        with patch('forum.models.Comment.objects.filter') as mock:
            mock.return_value = mock_queryset
            context = view.get_context_data()

        """結果の検証"""
        # contextにページネーション結果がセットされていることを検証
        self.assertIn('page_obj', context)
        self.assertEqual(context['page_obj'].object_list, mock_comments[3:])

    def test_get_context_data_not_found(self):
        """get_context_dataでページネーション結果が存在しない場合に例外が発生することを確認"""

        """手順の実施＆結果の検証"""

        view = UserDetail()
        view.object = self.user
        
        # リクエストを生成
        request = self.factory.get('/forum/comments/?p=3')
        request.user = self.user
        view.request = request

        # ５件分のレコードのモックを返却するモックのメソッドを作成
        mock_comments = [MagicMock() for _ in range(5)]
        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = mock_comments

        # filterメソッドにモックを仕掛けた状態でget_context_dataを実行
        with patch('forum.models.Comment.objects.filter') as mock:
            mock.return_value = mock_queryset

            # ページネーション結果が存在しない場合にEmptyPageが発生することを検証
            with self.assertRaises(EmptyPage):
                view.get_context_data()