from django.urls import path, include
from . import views

app_name ='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
]