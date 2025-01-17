from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from rest_framework.authtoken.models import Token
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from forum.models import Comment, CustomUser
import time

class LoginUITest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ドライバーを生成（Chromeが起動）
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # ドライバーを終了（Chromeが終了）
        cls.driver.quit()

        super().tearDownClass()

    def setUp(self):
        """各テストケースで毎回必要になる準備"""

        # ユーザーの作成
        self.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassss',
            age = 20,
            email='hanako@example.com'
        )

    def test_check_login_form_send_button(self):
        """ログインフォームから各種フィールドの値が送信されることを確認する"""
        
        """手順の実施"""
        
        # ログインページの表示
        url = self.live_server_url + '/forum/login/'
        self.driver.get(url)

        # ユーザー名とパスワードを入力
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_field.send_keys('Hanako')

        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_field.send_keys('ppaassss')

        # ログインボタンをクリック
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))
        )
        login_button.click()

        time.sleep(2)
    
        """結果の検証"""

        # 詳細情報ページにリダイレクトされることの検証
        self.assertEqual(self.driver.current_url, self.live_server_url + f'/forum/user/{self.user.id}')

        # ウェブブラウザに正しいトークンが保存されていることを確認
        saved_token = self.driver.execute_script("return window.localStorage.getItem('access_token');") # JavaScript実行
        answer_token = Token.objects.get(user=self.user).key
        self.assertEqual(saved_token, answer_token)

class PostUITest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ドライバーを生成（Chromeが起動）
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # ドライバーを終了（Chromeが終了）
        cls.driver.quit()

        super().tearDownClass()

    def setUp(self):
        """各テストケースで毎回必要になる準備"""

        # ユーザーの作成
        self.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassss',
            age = 20,
            email='hanako@example.com'
        )

        # ログインページの表示
        url = self.live_server_url + '/forum/login/'
        self.driver.get(url)

        # ユーザー名とパスワードを入力
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_field.send_keys('Hanako')

        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_field.send_keys('ppaassss')

        # ログインボタンをクリック
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))
        )
        login_button.click()

        # リダイレクトされるまで待つ
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'h2'), 'Hanakoの情報'
            )
        )

    def test_check_post_form_send_button(self):
        """投稿フォームから各種フィールドの値が送信されることを確認する"""
        
        """手順の実施"""
        # コメント投稿ページを表示
        url = self.live_server_url + '/forum/post/'
        self.driver.get(url)

        # textフィールドを取得（表示されるまで待機）
        text_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )

        # textフィールドに文字列を入力
        text_field.send_keys('Yes!')

        # 送信ボタンを取得（クリックできるようになるまで待機）
        send_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@value="送信"]'))
        )

        # send_buttonをクリック
        send_button.click()

        # コメント一覧が表示されるまで待つ（コメント総数の要素が表示されるまで）
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'comment-count'))
        )

        """結果の検証"""

        # ボタンクリックによってコメントが追加されていることを検証
        comment = Comment.objects.all().last()

        self.assertEqual(comment.user.username, 'Hanako')
        self.assertEqual(comment.text, 'Yes!')

class CommentsUITest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ドライバーを生成（Chromeが起動）
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # ドライバーを終了（Chromeが終了）
        cls.driver.quit()

        super().tearDownClass()

    def setUp(self):
        """各テストケースで毎回必要になる準備"""

        # ユーザーの作成
        self.user = CustomUser.objects.create_user(
            username='Hanako',
            password='ppaassss',
            age = 20,
            email='hanako@example.com'
        )

        # ログインページの表示
        url = self.live_server_url + '/forum/login/'
        self.driver.get(url)

        # ユーザー名とパスワードを入力
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_field.send_keys('Hanako')

        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_field.send_keys('ppaassss')

        # ログインボタンをクリック
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))
        )
        login_button.click()

        # リダイレクトされるまで待つ
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'h2'), 'Hanakoの情報'
            )
        )


    def test_check_update_comment_count(self):
        """コメント一覧ページのコメント総数が動的更新されることを確認する"""

        """手順の実施"""
        # フォームを表示するURLを設定
        url = self.live_server_url + '/forum/comments/'

        # ウェブブラウザでurlを開く
        self.driver.get(url)

        # コメント総数が表示されるまで待機
        comment_count_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'comment-count'))
        )

        # ページに表示されているコメント総数を取得
        before_comment_count = int(comment_count_elem.text)

        # コメントを追加
        Comment.objects.create(user=self.user, text='Yes!')
        time.sleep(2)

        # ページに表示されているコメント総数を取得
        after_comment_count = int(comment_count_elem.text)

        """結果の検証"""
        # コメントの追加に伴って表示されているコメント総数が動的更新されることを検証
        self.assertEqual(before_comment_count + 1, after_comment_count)