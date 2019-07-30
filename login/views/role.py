from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from login.models import Role
from login.serializers import RoleSerializer


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