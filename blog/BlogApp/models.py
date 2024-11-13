from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=25)
    subscription = models.CharField(max_length=100)
    photo_post = models.ImageField(default=None, upload_to='img/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.title} / {self.author}"

    def toggle_like(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def likes_count(self):
        return self.likes.count()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_users', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')  # Garante que cada relacionamento seja único

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def save(self, *args, **kwargs):
        """Ao salvar um novo 'follow', atualiza a contagem de seguidores."""
        super().save(*args, **kwargs)
        self.following.profile.update_followers_count()

    def delete(self, *args, **kwargs):
        """Ao deletar um 'follow', atualiza a contagem de seguidores."""
        super().delete(*args, **kwargs)
        self.following.profile.update_followers_count()





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)  # Novo campo para contagem de seguidores

    def __str__(self):
        return f"Profile of {self.user.username}"

    def update_followers_count(self):
        """Atualiza o campo followers_count com a contagem atual de seguidores."""
        self.followers_count = Follow.objects.filter(following=self.user).count()
        self.save()


    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"

    def clean(self):
        if not self.content.strip():
            raise ValidationError("O conteúdo do comentário não pode ser vazio.")
        if len(self.content) > 500:
            raise ValidationError("O comentário não pode ter mais de 500 caracteres.")

    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Impede múltiplos likes do mesmo usuário no mesmo post

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
