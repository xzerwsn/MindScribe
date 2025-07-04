from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'github', 'vk', 'telegram', 'discord']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'vk': forms.URLInput(attrs={'placeholder': 'https://vk.com/username'}),
            'telegram': forms.TextInput(attrs={'placeholder': '@username'}),
            'discord': forms.TextInput(attrs={'placeholder': 'username#1234'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_file', 'tags']  # Убрали media_type из fields
        
        widgets = {
            'media_file': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.gif,.svg,.mp4,.webm,.avi'
            })
        }