from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.models import ApiUser, Content
from api.serializers import ApiUserSerializer, ContentSerializer


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ApiUserListView(generics.ListCreateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = ApiUserSerializer
    queryset = ApiUser.objects.all()


class ContentView(generics.ListCreateAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        filter = {'is_premium': False}
        if self.request.user.apiuser.is_premium:
            filter['is_premium'] = True
        return Content.objects.filter(**filter)