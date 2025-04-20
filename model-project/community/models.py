from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Category choices for posts
CATEGORY_CHOICES = [
    ('general', 'General Discussion'),
    ('crop_disease', 'Crop Diseases'),
    ('farming_tips', 'Farming Tips'),
    ('market_info', 'Market Information'),
    ('tech', 'Agricultural Technology'),
    ('question', 'Questions'),
]

def validate_file_size(value):
    """Validate that the file size is under 5MB"""
    filesize = value.size
    
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    return value

class Post(models.Model):
    """Model for community forum posts"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='community_posts/%Y/%m/', blank=True, null=True, validators=[validate_file_size])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
        
    def get_like_count(self):
        return self.likes.count()
        
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    """Model for comments on posts, with support for threaded replies"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
        
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})
