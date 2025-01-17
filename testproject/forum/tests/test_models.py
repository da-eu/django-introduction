from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from forum.models import Comment, CustomUser

class CommentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """各テストケースで共通で必要となるレコードの準備"""

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

        Comment.objects.create(
            user=cls.user,
            text='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )

    def test_create_comment_success(self):
        """各種フィールドが正常な場合にレコードの新規登録に成功することを確認する"""

        """手順の実施"""

        # 時間計測のための現在時刻を取得
        now = timezone.now()

        # レコードの新規登録
        comment = Comment()
        comment.user = self.user
        comment.text = 'Yes'
        comment.save()

        """結果の検証"""
        # 新規登録したレコードを取得
        comment = Comment.objects.get(id=3)
        
        # 各種フィールドの値が正しいことを検証
        self.assertEqual(comment.user.username, 'Hanako')
        self.assertEqual(comment.text, 'Yes')

        # 作成日時がほぼ現在時刻であることを検証
        self.assertTrue(comment.date >= now)
        self.assertTrue(comment.date < now + timezone.timedelta(seconds=1))

    def test_create_comment_text_null(self):
        """textフィールドが無しの場合にレコードの新規登録に失敗することを確認する"""

        """手順の実施＆結果の検証"""
        # textフィールドが無しのレコードを作成
        comment = Comment()
        comment.user = self.user
        comment.text = None

        # レコードの新規登録の実行＆例外発生の検証
        with self.assertRaises(IntegrityError):
            comment.save()

    def test_get_comments_success(self):
        """全てのコメントが取得できることを確認する"""

        """手順の実施"""
        # 全コメントの取得
        comments = Comment.objects.all()

        """結果の検証"""
        # コメントの数が正しいことを検証
        self.assertEqual(len(comments), 2)

    def test_str_success(self):
        """__str__メソッドが正常に動作することを確認する"""

        """手順の実施"""
        # __str__メソッドの実行
        comment = Comment.objects.get(id=2)
        result = comment.__str__()

        """結果の検証"""
        # __str__から正しい文字列が返却されることを検証
        self.assertEqual(result, 'ABCDEFGHIJ')