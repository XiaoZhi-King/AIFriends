from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenView(APIView):
   def post(self, request, *args, **kwargs):
       try:
            refresh_token = request.COOKIES.get('refresh_token') #从cookie中获取refresh_token
            if not refresh_token:
                return Response({
                    'result' : 'refresh_token不存在'
                }, status=401)
            refresh = RefreshToken(refresh_token) #如果refresh_token过期，会抛出异常
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti()
                response = Response({
                    'result' : 'success',
                    'access' : str(refresh.access_token),
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=False,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result' : 'success',
                'access' : str(refresh.access_token),
            })
       except:
           return Response({
               'result' : '系统异常，请稍后再试'
           }, status=401) #必须加401
