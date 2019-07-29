from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from passlib.hash import pbkdf2_sha256

from .models import Role, User
from .serializers import RoleSerializer, UserSerializer


def get_hashed_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=20)


class RoleView(APIView):
    """
        List all roles, or create new role
    """
    def get(self, request):
        roles = Role.objects.all()
        serialized_roles = RoleSerializer(roles, many=True)
        return Response(serialized_roles.data)

    def post(self, request):
        serialized_role = RoleSerializer(data=request.data)
        if serialized_role.is_valid():
            serialized_role.save()
            return Response(serialized_role.data, status=status.HTTP_201_CREATED)
        return Response(serialized_role.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDetail(APIView):
    """
        Retrieve, update or delete a role instance.
    """
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        role = self.get_object(pk)
        serialized_role = RoleSerializer(role)
        return Response(serialized_role.data)

    def put(self, request, pk, format=None):
        role = self.get_object(pk)
        serialized_role = RoleSerializer(role, request.data)
        if serialized_role.is_valid():
            serialized_role.save()
            return Response(serialized_role.data)
        return Response(serialized_role.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        role = self.get_object(pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            hased_password = get_hashed_password(user_data.get('password'))
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
            hased_password = get_hashed_password(user_request_data.get('password'))
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
