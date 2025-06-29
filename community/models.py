from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Post model for community posts
    """
    POST_TYPE_CHOICES = [
        ('job', 'Job'),
        ('project', 'Project'),
        ('internship', 'Internship'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.created_by.get_full_name()}"
    
    def get_post_type_display_name(self):
        return dict(self.POST_TYPE_CHOICES)[self.post_type]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.post.title}"

class DirectMessage(models.Model):
    """
    Direct Message model for private conversations
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.get_full_name()} to {self.recipient.get_full_name()}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    @classmethod
    def get_conversation(cls, user1, user2):
        """
        Get all messages between two users
        """
        return cls.objects.filter(
            models.Q(sender=user1, recipient=user2) | 
            models.Q(sender=user2, recipient=user1)
        ).order_by('created_at')
    
    @classmethod
    def get_unread_count(cls, user):
        """
        Get count of unread messages for a user
        """
        return cls.objects.filter(recipient=user, is_read=False).count()
