from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import LeaveRequestSerializer
from .models import LeaveRequest
from .permissions import IsManager
from rest_framework.permissions import IsAuthenticated
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
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MyLeaveRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        status_param = request.GET.get('status')
        leaves = LeaveRequest.objects.filter(user=request.user)
        if status_param:
            leaves = leaves.filter(status=status_param)
        serializer = LeaveRequestSerializer(leaves,many=True)
        return Response(serializer.data)

class ApproveLeaveView(APIView):
    permission_classes = [IsAuthenticated,IsManager]

    def post(self,request,id):
        leave = LeaveRequest.objects.get(id=id)
        if leave.status != 'pending':
            return Response({'error':'Leave Request Already Processed'},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            leave.status = 'approved'
            leave.save()
            return Response({'message': 'Leave Request Approved Successfully'},status=status.HTTP_200_OK)
        
class RejectLeaveView(APIView):
    permission_classes = [IsAuthenticated,IsManager]
    def post(self,request,id):
        leave = LeaveRequest.objects.get(id=id)
        if leave.status != 'pending':
            return Response({'error':'Leave Request Already Processed'},status=status.HTTP_400_BAD_REQUEST)
        else:
            leave.status = 'rejected'
            leave.save()
            return Response({'message':'Leave Request Rejected Successfully'},status=status.HTTP_200_OK)
        
class AllLeaveRequestView(APIView):
    permission_classes = [IsAuthenticated,IsManager]
    def get(self,request):
        leaves = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leaves,many= True)
        return Response(serializer.data)