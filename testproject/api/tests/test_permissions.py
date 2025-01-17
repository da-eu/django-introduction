from django.test import TestCase, RequestFactory
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from api.permissions import IsAuthorOrReadOnly
from forum.models import Comment, CustomUser

class IsAuthorOrReadOnlyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるレコードの準備"""

        # ユーザーの作成
        cls.user1 = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
        )

        cls.user2 = CustomUser.objects.create_user(
            username='Taro',
            password='ppaassww',
            age = 20,
        )

        # コメントの作成
        cls.comment = Comment.objects.create(
            user=cls.user1,
            text='Hello'
        )

    def setUp(self):
        """各テストケースで毎回必要となる準備を実施"""

        self.factory = RequestFactory()
        
    def test_has_object_permission_true(self):
        """操作対象のレコードの作成者とリクエストユーザーが一致する場合にTrueを返却することを確認する"""

        """手順の実施"""

        # リクエストユーザーをuser1に設定
        request = self.factory.patch('/api/comments/1')
        request.user = self.user1

        # has_object_permissionメソッドの実行
        permission = IsAuthorOrReadOnly()
        result = permission.has_object_permission(request, None, self.comment)
        
        """結果の検証"""
        # Trueが返却されることを検証
        self.assertTrue(result)

    def test_has_object_permission_false(self):
        """操作対象のレコードの作成者とリクエストユーザーが一致しない場合にFalseを返却することを確認する"""
        
        """手順の実施"""
        # リクエストユーザーをuser2に設定
        request = self.factory.patch('/api/comments/1')
        request.user = self.user2

        # has_object_permissionメソッドの実行
        permission = IsAuthorOrReadOnly()
        result = permission.has_object_permission(request, None, self.comment)
        
        """結果の検証"""
        # Falseが返却されることを検証
        self.assertFalse(result)

    def test_has_object_permission_read_only(self):
        """リクエストメソッドがGETの場合にTrueを返却することを確認する"""

        """手順の実施"""
        # リクエストユーザーをuser2に設定
        request = self.factory.get('/api/comments/1')
        request.user = self.user2

        # has_object_permissionメソッドの実行
        permission = IsAuthorOrReadOnly()
        result = permission.has_object_permission(request, None, self.comment)
        
        """結果の検証"""
        # Trueが返却されることを検証
        self.assertTrue(result)