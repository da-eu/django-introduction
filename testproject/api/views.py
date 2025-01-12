from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from forum.models import Comment
from .serializers import CommentSerializer
from .filters import CommentFilter
from .permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    ### コメントの操作API
    #### 認証
    - トークン認証
    #### 権限
    - 認証に失敗した場合はAPIの実行は失敗します
    - 他のユーザーが作成したレコードの更新・削除はできません
    #### その他
    - コメントの投稿者にはコメントの新規登録APIを実行したユーザーが自動的に設定されます
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoginAPI(APIView):

    @swagger_auto_schema(
        operation_description="ログインして認証トークンを取得します。",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='ユーザー名'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='パスワード'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='認証トークン'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ユーザーID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='ユーザー名'),
                },
            ),
            400: "Invalid credentials",
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # ユーザー認証
        user = authenticate(username=username, password=password)

        if user is not None:
            # 認証成功時にトークンを発行
            token, created = Token.objects.get_or_create(user=user)

            login(request, user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            }, 200)
        else:
            return Response({
                'detail': '提供された認証情報でログインできません',
            }, 400)



class LogoutAPI(APIView):

    @swagger_auto_schema(
        operation_description="ログアウトして認証トークンを削除します。",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='ログアウトに成功しました'),
                },
            ),
        },
    )
    def post(self, request):
        if request.user.is_authenticated:
            # ログイン中のユーザーに対してのみ下記を実施

            # 現在のユーザーに紐付いたトークンを削除
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
            except Token.DoesNotExist:
                pass

            logout(request)

        return Response({
            'detail': 'ログアウトに成功しました',
        }, 200)