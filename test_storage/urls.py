from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.video, name='videos'),
    path('photos/', views.photo, name='photos'),
    path('audios/', views.audio, name='audios'),
]
