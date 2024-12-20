from django.http import JsonResponse

class LoginRequiredAPIMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': '認証に失敗しました'}, status=401)
        return super().dispatch(request, *args, **kwargs)