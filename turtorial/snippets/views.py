from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from snippets.serializers import SnippetSerializer
from snippets.models import Snippet


@csrf_exempt
def snippet_list(request):
    """列出所有snippet对应的json字段"""

    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.errors, status=400)
