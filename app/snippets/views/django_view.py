from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from ..serializers import SnippetListSerializer
from ..models import Snippet

__all__ = (
	'snippet_list',
	'snippet_detail',
)



class JsonResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super().__init__(content, **kwargs)

@csrf_exempt
def snippet_list(request):
	if request.method =='GET':
		snippets = Snippet.objects.order_by('-created')
		serializer = SnippetListSerializer(snippets, many=True)
		json_data = JSONRenderer().render(serializer.data)
		return HttpResponse(json_data, content_type='application/json')
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetListSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
	"""
	코드 조각 조회, 업데이트, 삭제
	:param request:
	:param pk:
	:return:
	"""

	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SnippetListSerializer(snippet)
		return JsonResponse(serializer.data)

	elif request.method == 'PATCH':
		data = JSONParser().parse(request)
		serializer = SnippetListSerializer(snippet, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204)

