from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status

# viewset
from rest_framework import viewsets

from . import models
from . import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework .authentication import TokenAuthentication
from rest_framework import filters

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated



class HelloApiView(APIView):

    serializer_class = serializers.HelloSerizlizer

    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods as function',
            'Some text here'
        ]

        return Response({'message':'Hello world', 'an_apiview':an_apiview})

    def post(self, request):
        serializer = serializers.HelloSerizlizer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message =  f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method':'put'})

    def patch(self,request, pk=None):
        return Response({'method':'path'})

    def delete(self, requset, pk=None):
        return Response({'method':'delete'})





class HelloViewSet(viewsets.ViewSet):

    def list(self, request):
        a_viewset = [
            'Uses actions like apiView',
            'Automatically map something'
        ]

        return Response({'message':'Hello', 'a_viewset':a_viewset})






class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnPermmissins, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email',)



class LoginViewSet(viewsets.ViewSet):

    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().post(request)



class UserProfileFeedViewset(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)


    def perform_create(self, serializer):
        serializer.save(user_profile = self.request.user)