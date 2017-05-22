from django.core.serializers import json
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import Http404
from django.core import serializers


from api.apiwrapper import TCOL
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
import os


@csrf_protect
#@api_view(['GET', 'PUT', 'DELETE'])
#def profile_page(request, location):
def api_view(request):
    if request.method == 'GET':
        location = request.GET['q']
        mydata = TCOL.get_topsongs(location)
        return HttpResponse(json.dumps(mydata), content_type="application/json")






'''
@csrf_protect
def food_search(request):
    keyword = request.GET['q']
    items = FCD.find(keyword)
    return HttpResponse(json.dumps(items), content_type="application/json")

'''
