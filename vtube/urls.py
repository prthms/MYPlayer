from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('trending', views.getTrending, name="Trending"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('channel/<int:id>', views.handleChannel, name="handleChannel"),
    path('create-channel', views.CreateChannel, name="CreateChannel"),
    path('upload-video', views.UploadVideo, name="UploadVideo"),
    path('upload-video-save', views.UploadVideoSave, name="UploadVideoSave"),
    path('channel-about/<int:id>', views.ChannelAbout, name="ChannelAbout"),
    path('getvideos', views.getVideos, name="getVideos"),
    path('watch/<int:id>', views.watchVideo, name="watchVideo"),
    path('edit-video/<int:id>', views.editVideo, name="editVideo"),
    path('your-videos', views.yourVideo, name="YourVideo"),
    path('history', views.userHistoryFunc, name="userHistory"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
