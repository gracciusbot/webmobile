from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from BlogApp.models import Post, Follow, Comment, Profile
from .serializers import LoginSerializer, PostSerializer, FollowSerializer, CommentSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


# Home View
class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns the list of posts with their comments.
        """
        user_profile, _ = Profile.objects.get_or_create(user=self.request.user)
        posts = Post.objects.all()  # You can filter posts if necessary
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]  # Permite que qualquer um acesse (sem estar autenticado)
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Verifica se ambos os campos foram enviados
        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        # Autentica o usuário
        user = authenticate(username=username, password=password)

        if user:
            # Se o usuário existe, gera um token
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


# Like Post View
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Alterna o like no post. Se o usuário já curtiu, remove o like.
        """
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        # Chama o método toggle_like no modelo para adicionar ou remover o like
        post.toggle_like(user)

        # Retorna a contagem de likes atualizada
        return Response({"likes_count": post.likes_count()}, status=status.HTTP_200_OK)

# Post CRUD
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Cria o post com o autor sendo o usuário autenticado
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = super().get_object()
        if not (post.author == self.request.user or self.request.user.is_staff):
            raise PermissionDenied("Você não tem permissão para editar ou excluir este post.")
        return post


# Follow CRUD
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]  # Garantir que o usuário esteja logado
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id):
        """
        Seguir ou deixar de seguir um usuário.
        """
        user_to_follow = get_object_or_404(User, id=user_id)

        # Verifica se o usuário está tentando se seguir
        if user_to_follow == request.user:
            return Response({'error': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se já existe um relacionamento de follow
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if not created:
            follow.delete()  # Deixar de seguir
            following = False
        else:
            following = True  # Seguir

        # Contagem de seguidores
        followers_count = Follow.objects.filter(following=user_to_follow).count()

        return Response({
            'following': following,
            'followers_count': followers_count
        })


# Comment CRUD
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Garantir que o usuário esteja logado

    def post(self, request, post_id):
        """
        Cria um novo comentário para o post especificado
        """
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')  # O conteúdo do comentário vem no corpo da requisição

        if not content:
            return Response({"error": "O conteúdo do comentário não pode ser vazio."}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )

        # Retornar o comentário recém-criado
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        if not (comment.author == self.request.user or self.request.user.is_staff):
            raise PermissionDenied("Você não tem permissão para editar ou excluir este comentário.")
        return comment


# Profile CRUD
# Profile Create View
class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Garantir que o usuário esteja logado

    def post(self, request):
        """
        Cria um novo perfil para o usuário autenticado
        """
        user = request.user  # O perfil será criado para o usuário autenticado
        data = request.data
        data['user'] = user.id  # Associando o perfil ao usuário

        serializer = ProfileSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()  # Salva o perfil no banco de dados
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile Detail View
class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = super().get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Você não tem permissão para editar ou excluir este perfil.")
        return profile
