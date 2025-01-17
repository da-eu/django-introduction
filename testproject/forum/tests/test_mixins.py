from unittest.mock import MagicMock, patch
from django.test import TestCase, RequestFactory
from forum.models import Comment, CustomUser
from forum.mixins import AuthorRequiredMixin


class AuthorRequiredMixinTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるレコードの準備"""

        # ユーザーの作成
        cls.user1 = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
            email='hanako@example.com'
        )

        cls.user2 = CustomUser.objects.create_user(
            username='Taro',
            password='ppaassww',
            age = 20,
            email='taro@example.com'
        )

        # user1によるコメントの作成
        cls.comment = Comment.objects.create(
            user=cls.user1,
            text='Hello'
        )

    def setUp(self):
        self.factory = RequestFactory()

    def test_test_func_true(self):
        """操作対象のレコードの作成者とリクエストユーザーが一致する場合にTrueを返却することを確認する"""

        """手順の実施"""
        mixin = AuthorRequiredMixin()

        # リクエストユーザーをuser1に設定
        mixin.request = self.factory.delete('/forum/comment/1')
        mixin.request.user = self.user1

        # get_objectをモックに差し替えてtest_funcメソッドを実行
        mock = MagicMock(return_value=self.comment)
        mixin.get_object = mock
        result = mixin.test_func()

        """結果の検証"""
        # Trueが返却されることを検証
        self.assertTrue(result)

    def test_test_func_false(self):
        """操作対象のレコードの作成者とリクエストユーザーが一致しない場合にFalseを返却することを確認する"""
        
        """手順の実施"""
        mixin = AuthorRequiredMixin()

        # リクエストユーザーをuser2に設定
        mixin.request = self.factory.delete('/forum/comment/1')
        mixin.request.user = self.user2
 
        # get_objectをモックに差し替えてtest_funcメソッドを実行
        mock = MagicMock(return_value=self.comment)
        mixin.get_object = mock
        result = mixin.test_func()

        """結果の検証"""
        # Falseが返却されることを検証
        self.assertFalse(result)