from django import forms
from .models import Knowledge, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KnowledgeForm(forms.ModelForm):
    class Meta:
        model=Knowledge
        fields=['title','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['text']
        widgets={
            'text':forms.Textarea(attrs={'row':3}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar', 'bio']
        labels = {
            'display_name': '表示名',
            'avatar': 'プロフィール画像',
            'bio': '自己紹介',
        }
        widgets = {
            'avatar': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'password1', 'password2']