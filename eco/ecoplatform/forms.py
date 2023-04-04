from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'text-field', 'placeholder': 'Your name'}),
            # 'email': forms.EmailInput(attrs={'class': 'text-field', 'placeholder': 'Your email'}),
            'text': forms.Textarea(attrs={'class': 'text-field', 'placeholder': 'Leave a comment'}),
        }
