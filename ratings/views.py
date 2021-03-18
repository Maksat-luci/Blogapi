from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.serializers import CreateRatingSerializer


class AddStarRatingView(APIView):

    def post(self, request):

        serializer = CreateRatingSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)
