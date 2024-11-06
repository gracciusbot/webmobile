from django.urls import path
from .views import LoginView, PostListCreateView, PostDetailView, FollowUserView, CommentListCreateView, CommentDetailView, ProfileDetailView, LikePostView

urlpatterns = [
    # Post URLs
    path('posts/', PostListCreateView.as_view(), name='api_post_list_create'),  # Listar e criar posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='api_post_detail'),  # Detalhar, atualizar e excluir posts

    # Follow URLs
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='api_follow_user'),  # Seguir e deixar de seguir usuários

    # Comment URLs
    path('comments/', CommentListCreateView.as_view(), name='api_comment_list_create'),  # Listar e criar comentários
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='api_comment_detail'),  # Detalhar, atualizar e excluir comentários

    # Profile URLs
    path('profile/', ProfileDetailView.as_view(), name='api_profile_detail'),  # Obter o perfil do usuário

    # Post Like URLs
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like_post'),

    #TOKEN LOGIN
    path('api/token/', LoginView.as_view(), name='api_token_login'),
]
