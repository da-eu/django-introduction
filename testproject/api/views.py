from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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