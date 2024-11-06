from django.contrib import admin
from .models import Post, Follow, Comment, Profile, Like

class LikeAdmin(admin.ModelAdmin):
    list_display=('user', 'post')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'followers_count')
    
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author','content','created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'photo_post', 'updated_at', 'get_author', 'get_likes_count')

    def get_author(self, obj):
        return obj.author.username  # Ajuste conforme o seu modelo
    get_author.short_description = 'Author'

    def get_likes_count(self, obj):
        return obj.likes.count()  # Supondo que likes seja um campo de muitos-para-muitos
    get_likes_count.short_description = 'Likes Count'

admin.site.register(Follow, FollowAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Like, LikeAdmin)
