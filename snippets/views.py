from django.http import Http404
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

# Create your views here.
class SnippetList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self,request,format=None):
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer=SnippetSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def pre_save(self,obj):
        obj.owner=self.request.user
#111
class SnippetDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    def get_object(self,pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Http404
    def get(self,request,pk,format=None):
        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet,request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        snippet=self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def pre_save(self,obj):
        obj.owner=self.request.user

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer