from rest_framework import mixins,status, viewsets,generics
from authentication.serializer import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from . models import User
from . utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError


# Create your views here.

class SignupViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data.copy() if request.data else {}
        serializer_class = SignupCreateSerializer(data = data, context = {"request":request})
        if serializer_class.is_valid():
            serializer_class.save()
            user_data = serializer_class.data
            user = User.objects.get(email=user_data['email'])

            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('activate')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            body ='Hi'+' '+user.username+' '+'use link below to verify your email\n'+ absurl
            data = {'body': body,'to':user.email,'subject':'Verify your Email'}
            Util.send_email(data)
           
            return Response({"email": serializer_class.data['email'], "username": serializer_class.data['username']},status= status.HTTP_201_CREATED)
        else:
            raise ValidationError
            return Response(ValidationError,status= status.HTTP_400_BAD_REQUEST)

class Activate(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id = payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()                
            return Response({'message': 'Succesfully Activated!'},status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'Error': 'Link Expired!'},status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'Error': 'Invalid token!'},status= status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

