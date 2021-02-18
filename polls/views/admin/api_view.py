from rest_framework import authentication, permissions
from rest_framework.views import APIView


class AdminAPIView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
