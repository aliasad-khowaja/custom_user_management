import ujson, jwt
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from login.models import User

from login.helper import Helper

SECRET_KEY = 'DGS_SECRET_KEY'


class LoginView(APIView):

    def post(self, request):

        if not (request.data and request.data.get('username') and request.data.get('password')):
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'Error': "Invalid username/password"}, status="400")

        if user:
            if Helper.check_hashed_password(password, user.password):
                payload = {
                    'username': user.username,
                    'role': user.role.id
                }
                jwt_token = {'token': jwt.encode(payload, SECRET_KEY, algorithm='HS256')}
                return HttpResponse(
                    ujson.dumps(jwt_token),
                    status=200,
                    content_type="application/json"
                )

        return HttpResponse(
            ujson.dumps({'Error': 'Invalid credentials'}),
            status=400,
            content_type="application/json"
        )