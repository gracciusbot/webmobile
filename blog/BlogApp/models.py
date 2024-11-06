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

    def clean(self):
        if len(self.title) > 25:
            raise ValidationError('O título não pode ter mais de 25 caracteres.')
        if len(self.subscription) > 100:
            raise ValidationError('A descrição não pode ter mais de 100 caracteres.')

    def is_liked_by(self, user):
        return user in self.likes.all()

    def likes_count(self):
        return self.likes.count()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_users', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')  # Impede duplicatas

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def followers_count(self):
        # Conta os seguidores a partir do modelo Follow, onde a pessoa é 'following'
        return Follow.objects.filter(following=self.user).count()

    followers_count.short_description = 'Contagem de Seguidores'

    def __str__(self):
        return f"Profile of {self.user.username}"

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Impede múltiplos likes do mesmo usuário no mesmo post

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
