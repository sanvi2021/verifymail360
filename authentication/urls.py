from django.urls import path
from .views import *


from .views import SignupViewSet, Activate
urlpatterns = [
    path("signup/",SignupViewSet.as_view({"post": "create"}), name= "Signup"),
    path('activate/',Activate.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('reset-password/', UserPasswordResetView.as_view(), name='user_password_reset'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
]