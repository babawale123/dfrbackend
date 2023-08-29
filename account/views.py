from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, authentication

@api_view(['POST'])
def SignUp(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username= request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token':token.key, 'user':serializer.data})
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
def Login(request):
    user = get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({msg:'password is incorrect'})
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token':token.key, 'user':serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllUser(request):
    username = [user.username for user in User.objects.all()]
    return Response(username)

class AllUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # def get(self,request, format=None):
    #     # username = [user.username for user in User.objects.all()]
    #     return Response({"only authenticated user can see this route"})
    
    def get(self,request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data )


@api_view(['POST', 'GET','PUT','DELETE'])
def detailView(request,pk):
    
    try:
        user = User.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(User, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        return Response({"deleted successfully"})

class NewDetailView(APIView):
    
    def get(self,request,pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def post(request,pk):
        user = User.objects.get()
        serializer = UserSerializer(instance=user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("updated successfully")

def updateUser(request,pk):
    user = User.objects.get(pk=pk)
    serializer = UserSerializer(instance=user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)   

    