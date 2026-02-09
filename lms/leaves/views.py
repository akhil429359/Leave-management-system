from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import LeaveRequestSerializer
from .models import LeaveRequest
# Create your views here.

class LoginView(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if  not user:
            return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response({'token':token.key,'username':user.username,'is_staff':user.is_staff})
    
class ApplyLeaveView(APIView):
    def post(self,request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            print(request.user)
            print(request.user.is_authenticated)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MyLeaveRequestView(APIView):
    def get(self,request):
        leaves = LeaveRequest.objects.filter(user=request.user)
        serializer = LeaveRequestSerializer(leaves,many=True)
        return Response(serializer.data)
