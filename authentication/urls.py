from django.contrib import admin
from django.urls import path
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

from .views import SignupViewSet, Activate
urlpatterns = [
    path("admin/", admin.site.urls),
    path("singup/",SignupViewSet.as_view({"post": "create"}), name= "Signup"),
    path('activate/<uidb64>/<token>/',Activate.as_view({"get":"retrieve"}), name='activate')
]