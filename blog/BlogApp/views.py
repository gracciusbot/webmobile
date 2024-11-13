from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Follow, Comment, Profile, Like
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from BlogApp.forms import ProfileForm, CommentForm

# View para a página inicial exibindo os posts
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adiciona a lista de comentários para cada post
        for post in context['posts']:
            post.comments_list = list(post.comments.all())
            

        # Obter o perfil do usuário atual
        user_profile, _ = Profile.objects.get_or_create(user=self.request.user)

        # Obter os IDs dos posts que o usuário curtiu
        liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context['liked_posts'] = set(liked_posts)

        # Obter os usuários que o usuário atual está seguindo
        user_following = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        context['user_following'] = set(user_following)

        return context

# View para curtir/descurtir um post
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
        return redirect('home')
        
        
# View para ver detalhes do post
class PostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comments = post.comments.all()  # Obter todos os comentários do post
        form = CommentForm()  # Formulário vazio para ser preenchido

        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, "Comentário adicionado com sucesso.")
        else:
            messages.error(request, "Erro ao adicionar o comentário. Por favor, tente novamente.")
        
        return redirect('post_detail', pk=post.id)

    
# View para seguir/desseguir um usuário
class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return JsonResponse({'error': 'Você não pode seguir a si mesmo.'}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if not created:
            follow.delete()  # Deixar de seguir
            following = False
        else:
            following = True  # Seguir

        # Contagem de seguidores
        followers_count = Follow.objects.filter(following=user_to_follow).count()

        # Passa o status de "seguindo" e a nova contagem de seguidores
        return JsonResponse({
            'following': following,
            'followers_count': followers_count
        })
# View para registrar usuário
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "O nome de usuário já existe.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está registrado.")
            return render(request, 'register.html')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)
        )
        user.save()
        messages.success(request, "Registro realizado com sucesso! Você pode entrar agora.")
        return redirect('login')

# View para perfil do usuário
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_to_view = self.object
        context['profile_form'] = ProfileForm(instance=user_to_view.profile)  # Adicionando o formulário de perfil
        return context

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)  # Incluindo request.FILES para permitir o upload de arquivo

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
        else:
            messages.error(request, "Erro ao atualizar o perfil.")
        
        return redirect('profile', pk=user.pk)

# View para login
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Credenciais inválidas')
        except User.DoesNotExist:
            messages.error(request, 'Usuário com este e-mail não existe')

        return render(request, self.template_name)

# Logout
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)  # Desconecta o usuário
        return redirect('/logout/')
