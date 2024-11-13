from django import forms
from .models import Profile, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # O campo content é o único que o usuário pode preencher.

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content.strip():  # Verifica se o conteúdo não é vazio ou só tem espaços
            raise forms.ValidationError("O conteúdo do comentário não pode ser vazio.")
        if len(content) > 500:  # Limita o conteúdo a 500 caracteres
            raise forms.ValidationError("O comentário não pode ter mais de 500 caracteres.")
        return content

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']  # Agora o formulário inclui a foto e a biografia

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Fale um pouco sobre você...'})
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) > 300:  # Limitar a biografia a 300 caracteres
            raise forms.ValidationError("A biografia não pode ter mais de 300 caracteres.")
        return bio