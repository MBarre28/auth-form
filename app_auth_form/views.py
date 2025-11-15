from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


def home(request):
    return HttpResponse('Authentication is now posted')

# authentication view

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    data = request.data
    return Response({
        'message': 'you are now logged successfully, enjoy!',
          'user': str(request.user),
          'data_retrived': data
          })


# registeration form
@api_view(['POST'])
@permission_classes([AllowAny])

def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not username or not password or not email:
        return Response({'required_field': 'username, password and email required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # conditional statement to check if username already exists

    if UserProfile.objects.filter(username=username).exists():
        return Response({'incorrect_field': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = UserProfile.objects.create_user(
    username = username,
    password = password,
    email = email,
    first_name = first_name,
    last_name = last_name

    )

    # refresh token form for user
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'user has been created sucessfully', 
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }, status=status.HTTP_201_CREATED)

    


# login form 
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])

def login_form(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'required_field': 'username and password is required'}, status=status.HTTP_400_BAD_REQUEST) 
    
    user = authenticate(username=username, password=password)

    # refresh token for login user
    
    if user is None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'login_sucessful!',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    else:
        return Response({'error': 'Incorrect username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        




# refresh token
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])

def refresh_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({'error': 'request token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        refresh = refresh_token(refresh_token)
        access_token = refresh.access_token
        return Response({'access': str(access_token)}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'error': 'access token has been expired, try again!'}, status=status.HTTP_400_BAD_REQUEST)



        





