from rest_framework import generics, permissions, status
from BlogApp.models import Post, Follow, Comment, Profile
from .serializers import PostSerializer, FollowSerializer, CommentSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

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


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]  # Garantir que o usuário esteja logado

    def post(self, request, pk):
        """
        Adiciona ou remove um like de um post
        """
        post = get_object_or_404(Post, id=pk)

        # Verifica se o usuário já curtiu o post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response({"message": "Like removido com sucesso!"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({"message": "Like adicionado com sucesso!"}, status=status.HTTP_200_OK)


# Post CRUD
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post = super().get_object()
        if not (post.author == self.request.user or self.request.user.is_staff):
            raise PermissionDenied("Você não tem permissão para editar ou excluir este post.")
        return post


# Follow CRUD
class FollowUserView(APIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]  # Garantir que o usuário esteja logado

    def post(self, request, user_id):
        """
        Seguir ou deixar de seguir um usuário.
        """
        user_to_follow = get_object_or_404(User, id=user_id)

        # Verifica se o usuário está tentando se seguir
        if user_to_follow == request.user:
            return JsonResponse({'error': 'Você não pode seguir a si mesmo.'}, status=400)

        # Verifica se já existe um relacionamento de follow
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if not created:
            follow.delete()  # Deixar de seguir
            following = False
        else:
            following = True  # Seguir

        # Contagem de seguidores
        followers_count = Follow.objects.filter(following=user_to_follow).count()

        # Retorna o status de "seguindo" e a contagem de seguidores
        return JsonResponse({
            'following': following,
            'followers_count': followers_count
        })

# Comment CRUD
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        if not (comment.author == self.request.user or self.request.user.is_staff):
            raise PermissionDenied("Você não tem permissão para editar ou excluir este comentário.")
        return comment


# Profile CRUD
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
