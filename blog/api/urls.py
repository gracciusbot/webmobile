from django.urls import path
from .views import CommentCreateView, LoginView, PostListCreateView, PostDetailView, FollowUserView, CommentDetailView, ProfileCreateView, ProfileDetailView, LikePostView



urlpatterns = [
    # Post URLs
    path('posts/', PostListCreateView.as_view(), name='api_post_list_create'),  # Listar e criar posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='api_post_detail'),  # Detalhar, atualizar e excluir posts
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='api_post_like'),
    path('profile/', ProfileCreateView.as_view(), name='create_profile'),  # Criação de perfil para o usuário autenticado
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    # Follow URLs
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='api_follow_user'),  # Seguir e deixar de seguir usuários

    # Comment URLs
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='api_create_comment'),  # Criar comentário em um post
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='api_comment_detail'),  # Detalhar, atualizar e excluir comentários

    # Profile URLs
    # Post Like URLs
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='api_like_post'),

    #TOKEN LOGIN
    path('token/', LoginView.as_view(), name='api_token_login'),
] 
