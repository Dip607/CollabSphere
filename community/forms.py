from django import forms
from .models import Post, Comment, DirectMessage

# community/forms.py
from .models import AlumniStory

class AlumniStoryForm(forms.ModelForm):
    class Meta:
        model = AlumniStory
        fields = ['title', 'content']
        
class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter post title...'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Share your thoughts, opportunities, or questions...'
        })
    )
    post_type = forms.ChoiceField(
        choices=Post.POST_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment...'
        })
    )
    class Meta:
        model = Comment
        fields = ['content']

class DirectMessageForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Type your message...'
        })
    )
    class Meta:
        model = DirectMessage
        fields = ['message'] 