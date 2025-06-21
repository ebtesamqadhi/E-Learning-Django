from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('profile/<str:username>/',views.view_profile, name='view_profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
]