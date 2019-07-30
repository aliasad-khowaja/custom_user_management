from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from login.models import User
from login.serializers import UserSerializer

from login.helper import Helper


class UserView(APIView):
    """
        List all user, or create new user
    """
    def get(self, request):
        users = User.objects.all()
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data)

    def post(self, request):
        user_data = request.data.copy()
        if user_data.get('password'):
            hased_password = Helper.get_hashed_password(user_data.get('password'))
            user_data['password'] = hased_password
        serialized_user = UserSerializer(data=user_data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
        Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        user_request_data = request.data.copy()
        if user_request_data.get('password'):
            hased_password = Helper.get_hashed_password(user_request_data.get('password'))
            user_request_data['password'] = hased_password
        serialized_user = UserSerializer(user, user_request_data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
