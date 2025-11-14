from django.urls import path 
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('protected/', views.protected_view, name='protected'),

    # JWT token authentication endpoints 
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # register & login endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_form, name='login')

]


