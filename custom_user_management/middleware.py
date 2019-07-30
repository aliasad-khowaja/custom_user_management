import ujson, jwt

from django.http import HttpResponse

from login.models import User

SECRET_KEY = 'DGS_SECRET_KEY'


class AuthenticationMiddleware:

    def __init__(self , get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not self.is_permit_all_uri(request.path):
            if self.has_token(request.headers):
                if self.is_valid_token(request.headers.get('Authorization')):
                    pass
                else:
                    return HttpResponse(ujson.dumps({'Error': 'Invalid Token'}), status=400,
                                        content_type="application/json")
            else:
                return HttpResponse(ujson.dumps({'Error': "Token Required"}), status=400,
                                    content_type="application/json")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    @staticmethod
    def is_permit_all_uri(uri):
        permit_all_uris = [
            '/api/login'
        ]
        return uri in permit_all_uris

    @staticmethod
    def has_token(headers):
        return headers.get('Authorization')

    @staticmethod
    def is_valid_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithm='HS256')
            username = payload.get('username')
            user = User.objects.get(username=username)
            # todo: check if token present in user
        except Exception as e:
            print(e)
            return False

        return True
