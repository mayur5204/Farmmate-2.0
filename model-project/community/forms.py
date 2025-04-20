from django import forms
from .models import Post, Comment, CATEGORY_CHOICES

class PostForm(forms.ModelForm):
    """Form for creating and editing posts"""
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Share your thoughts, questions, or information...', 
            'rows': 5
        })
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']


class CommentForm(forms.ModelForm):
    """Form for creating comments"""
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Write your comment here...', 
            'rows': 3
        })
    )
    
    class Meta:
        model = Comment
        fields = ['content']