from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .QueryBuilder import QueryBuilder

def index(request):
    return render(request, "index.html")

class Query(APIView):
    def post(self,request):
        query = request.data["query"]
        qb = QueryBuilder(query)
        return Response({'ok':True,"data":qb.get_all()})