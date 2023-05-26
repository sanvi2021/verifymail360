from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.validators import ValidationError
from authentication.serializer import *
from rest_framework.response import Response
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

# Create your views here.



class SignupViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    @extend_schema(request=SignupCreateSerializer, responses=SignupSerializer)
    def create(self, request, *args, **kwargs):
        data = request.data.copy() if request.data else {}
        serializer_class = SignupCreateSerializer(data = data, context = {"request":request})
        if serializer_class.is_valid():
            serializer_class.save()
            current_site = get_current_site(request)
            user = User.objects.get(email=serializer_class.data['email'])
            mail_subject = 'Activate your account.' 
            message = f"Please click on the following link to activate Your Account {current_site.domain} {urlsafe_base64_encode(force_bytes(user.pk))}{default_token_generator.make_token(user)}"
            to_email = serializer_class.data['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            # email.send()
            return Response(status= status.HTTP_200_OK)
        else:
            return Response({"Message": "Entered details is not a valid response"},status= status.HTTP_400_BAD_REQUEST)

class Activate(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
        
    @action(methods=["GET"], detail=True)
    def activate(request, uidb64, token):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response ({"Message": "Thank you for your email confirmation. Now you can login your account."}, status= status.HTTP_200_OK)
        else:
            return Response ({"Message": "Invalid Link."}, status= status.HTTP_400_BAD_REQUEST)

