from django.shortcuts import render
from accounts.models import RequestCount
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status


class RequestCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request_count = RequestCount.objects.first()
        return Response({'requests': request_count.count if request_count else 0},
                        status=status.HTTP_200_OK)

    def post(self, request):
        RequestCount.objects.update_or_create(id=1, defaults={'count': 0})
        return Response({'message': 'Request count reset successfully.'},
                        status=status.HTTP_200_OK)
