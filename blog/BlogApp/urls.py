from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import HomeView, LikePostView, ProfileView, LoginView, LogoutView, RegisterView, PostView, FollowUserView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/like/<int:pk>', LikePostView.as_view(), name='like_post'),
    path('profile/', ProfileView.as_view(), name='profile'),  # Para o perfil do usuário atual
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_detail'),  # Para o perfil de outros usuários
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post/<int:pk>', PostView.as_view(), name='post_detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
