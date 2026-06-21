from django import forms
from .models import Knowledge, Comment
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

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'password1', 'password2']