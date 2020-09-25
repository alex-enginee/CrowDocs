"""users app"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views


urlpatterns = [
    # section for registering users
    path('register/', views.register, name='register'),

    # verification path
    path('verify/', views.verify, name='verify'),

    # here for login/logout existed users
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # user profile page, here avatars and so on
    path('profile/', views.user_profile, name='user_profile'),
]
