from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from snippets.serializers import SnippetSerializer
from snippets.models import Snippet


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """列出所有snippet对应的json字段"""

    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        # data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """更新、更改、删除snippet模型"""
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 基于类视图重写API
class SnippetList(APIView):
    """列出所有snippet对应的json字段"""

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """更新、更改、删除snippet模型"""

    def get(self, request, pk, format=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # data = JSONParser().parse(request)
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# advance 使用mixins，重写基于类视图API
from rest_framework import mixins
from rest_framework import generics


class SnippetListAdvan(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    """列出所有snippet对应的json字段"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetailAdvan(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    """更新、更改、删除snippet模型"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# high：最简洁。使用mixins，重写基于类视图API

class SnippetListHigh(generics.ListCreateAPIView):
    """列出所有snippet对应的json字段"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetailHigh(generics.RetrieveUpdateDestroyAPIView):
    """更新、更改、删除snippet模型"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
