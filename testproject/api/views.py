import json
from forum.models import Comment
from .mixins import LoginRequiredAPIMixin
from django.contrib.auth import login, logout
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': '無効なJSON形式です'}, status=400)
        
        # 妥当性の検証
        if 'username' not in body:
            return JsonResponse({'detail': 'usernameフィールドが存在しません'}, status=400)
        if not isinstance(body['username'], str):
            return JsonResponse({'detail': 'usernameフィールドの値には文字列を指定してください'}, status=400)

        if 'password' not in body:
            return JsonResponse({'detail': 'passwordフィールドが存在しません'}, status=400)
        if not isinstance(body['password'], str):
            return JsonResponse({'detail': 'passwordフィールドの値には文字列を指定してください'}, status=400)

        # 認証
        user = authenticate(request, username=body['username'], password=body['password'])
        if user is not None:
            # 認証に成功したのログインを実施
            login(request, user)
            return JsonResponse({'success': 'ログインに成功しました'}, status=200)
        else:
            return JsonResponse({'detail': 'ログインに失敗しました'}, status=400)
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPI(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'success': 'ログアウトに成功しました'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class CommentAPI(LoginRequiredAPIMixin, View):
    def get(self, request):
        # クエリパラメーター取得
        min_id = request.GET.get('min_id')
        max_id = request.GET.get('max_id')

        # 妥当性の検証
        if min_id is not None:
            try:
                min_id = int(min_id)
            except ValueError:
                return JsonResponse({'detail': 'min_idには整数を指定してください'}, status=400)
        
        if max_id is not None:
            try:
                max_id = int(max_id)
            except ValueError:
                return JsonResponse({'detail': 'max_idには整数を指定してください'}, status=400)
        
        # コメント一覧の取得
        comments = Comment.objects.all()

        if min_id is not None:
            # idがmin_id以上のレコードに絞る
            comments = comments.filter(id__gte=min_id)
            
        if max_id is not None:
            # idがmax_id以下のレコードに絞る
            comments = comments.filter(id__lte=max_id)
        
        # レスポンスのボディにセットするデータをリストで作成
        comment_list = []

        for comment in comments:
            comment_dict = {
                'id': comment.id,
                'user': comment.user.username,
                'text': comment.text,
                'date': comment.date
            }
            comment_list.append(comment_dict)
        
        # リストをJSONに変換したデータをボディとするレスポンスを返却
        return JsonResponse(comment_list, status=200, safe=False)

    def post(self, request):
        # ボディのデータの取得
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': '無効なJSON形式です'}, status=400)
        
        # 妥当性の検証
        if 'text' not in body:
            return JsonResponse({'detail': 'textフィールドが存在しません'}, status=400)
        if not isinstance(body['text'], str):
            return JsonResponse({'detail': 'textフィールドの値には文字列を指定してください'}, status=400)
        if len(body['text']) < 1 or len(body['text']) > 256:
            return JsonResponse({'detail': 'コメントの文字列長が不正です'}, status=400)


        # レコードの新規登録
        comment = Comment()
        comment.user = request.user
        comment.text = body['text']
        comment.save()

        # レスポンスのボディにセットするデータを辞書で作成
        comment_dict = {
            'id': comment.id,
            'user': comment.user.username,
            'text': comment.text,
            'date': comment.date
        }

        # 辞書をJSONに変換したデータをボディとするレスポンスを返却
        return JsonResponse(comment_dict, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class CommentDetailAPI(LoginRequiredAPIMixin, View):
    def get(self, request, id):
        # idが引数idと一致するレコードを取得
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return JsonResponse({'detail': 'レコードが存在しません'}, status=404)
        
        # レスポンスのボディにセットするデータを辞書で作成
        comment_dict = {
            'id': comment.id,
            'user': comment.user.username,
            'text': comment.text,
            'date': comment.date
        }

        # 辞書をJSONに変換したデータをボディとするレスポンスを返却
        return JsonResponse(comment_dict, status=200)
    
    def patch(self, request, id):
        # ボディのデータの取得
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': '無効なJSON形式です'}, status=400)
        
        # 妥当性の検証
        if 'text' not in body:
            return JsonResponse({'detail': 'textフィールドが存在しません'}, status=400)
        if not isinstance(body['text'], str):
            return JsonResponse({'detail': 'textフィールドの値には文字列を指定してください'}, status=400)
        if len(body['text']) < 1 or len(body['text']) > 256:
            return JsonResponse({'detail': 'コメントの文字列長が不正です'}, status=400)

        # idが引数idと一致するレコードを取得
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return JsonResponse({'detail': 'レコードが存在しません'}, status=404)
        
        if request.user != comment.user:
            # 他のユーザーのレコードは更新不可
            return JsonResponse({'detail': '他のユーザーのレコードは更新できません'}, status=403)

        # レコードの更新（部分的な更新）
        comment.text = body['text']
        comment.save()

        # レスポンスのボディにセットするデータを辞書で作成
        comment_dict = {
            'id': comment.id,
            'user': comment.user.username,
            'text': comment.text,
            'date': comment.date
        }

        # 辞書をJSONに変換したデータをボディとするレスポンスを返却
        return JsonResponse(comment_dict, status=200)
    
    def delete(self, request, id):
        # idが引数idと一致するレコードを取得
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return JsonResponse({'detail': 'レコードが存在しません'}, status=404)
        
        if request.user != comment.user:
            # 他のユーザーのレコードは削除不可
            return JsonResponse({'detail': '他のユーザーのレコードは削除できません'}, status=403)
        
        # レコードの削除
        comment.delete()

        # ボディ無しのレスポンスを返却
        return HttpResponse(status=204)