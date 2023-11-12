from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django.core.exceptions import ValidationError
from .models import Message

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        if not email.endswith('@wayne.edu'):
            raise ValidationError('You must use a wayne.edu email address')
        return email



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
<<<<<<< Updated upstream
        fields = ['text', 'chat_room']
=======
        fields = ['text', 'chat_room']
>>>>>>> Stashed changes
