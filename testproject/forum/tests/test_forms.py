from django.test import TestCase
from forum.models import Comment, CustomUser
from forum.forms import PostForm

class PostFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるレコードの準備"""

        # ユーザーの作成
        cls.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassww',
            age = 20,
            email='hanako@example.com'
        )

        # コメントの作成
        Comment.objects.create(
            user=cls.user,
            text='Hello'
        )

    def test_is_valid_text_equal_max_len(self):
        """各種フィールドの値が正常な場合にis_validがTrueを返却することを確認する"""

        """手順の実施"""

        # textフィールドの文字列長が256文字のフォームデータを作成
        data = {
            'text': 'x' * 256
        }

        # is_validメソッドの実行
        form = PostForm(data)
        result = form.is_valid()

        """結果の検証"""
        # Trueが返却されることを検証
        self.assertTrue(result)

    def test_is_valid_text_equal_min_len(self):
        """各種フィールドの値が正常な場合にis_validがTrueを返却することを確認する"""

        """手順の実施"""

        # textフィールドの文字列長が256文字のフォームデータを作成
        data = {
            'text': 'x'
        }

        # is_validメソッドの実行
        form = PostForm(data)
        result = form.is_valid()

        """結果の検証"""
        # Trueが返却されることを検証
        self.assertTrue(result)

    def test_is_valid_text_greater_than_max_len(self):
        """textフィールドの文字列長が256を超える場合にis_validがFalseを返却することを確認する"""

        """手順の実施"""
        # textフィールドの文字列長が257文字のフォームデータを作成
        data = {
            'text': 'x' * 257
        }
        
        # is_validメソッドの実行
        form = PostForm(data)
        result = form.is_valid()

        """結果の検証"""
        # 結果がFalseであることを検証
        self.assertFalse(result)

        # エラーメッセージが含まれていることを検証
        self.assertIn('text', form.errors)

    def test_is_valid_text_less_than_min_len(self):
        """textフィールドの文字列長が1未満の場合にis_validがFalseを返却することを確認する"""

        """手順の実施"""
        # textフィールドの文字列長が257文字のフォームデータを作成
        data = {
            'text': ''
        }
        
        # is_validメソッドの実行
        form = PostForm(data)
        result = form.is_valid()

        """結果の検証"""
        # 結果がFalseであることを検証
        self.assertFalse(result)

        # エラーメッセージが含まれていることを検証
        self.assertIn('text', form.errors)