from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not username:
            raise ValueError('Superusers must have a username.')
        extra_fields['username'] = username
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User Model for CollabSphere
    Uses email as the unique identifier for authentication
    """
    ROLE_CHOICES = [
        ('student', 'Current Student'),
        ('alumni', 'Alumni'),
        ('professor', 'Professor'),
    ]
    
    # Override username to be optional
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    
    # Use email as the primary identifier
    email = models.EmailField(unique=True)
    
    # Additional fields
    passout_batch = models.CharField(max_length=10, blank=True, null=True, help_text="Graduation year (e.g., 2024)")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Set email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']  # username required for superuser

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    def get_short_name(self):
        return self.first_name if self.first_name else self.email

class Notification(models.Model):
    """
    Notification model for user notifications
    """
    NOTIFICATION_TYPES = [
        ('comment', 'New Comment'),
        ('reply', 'Reply to Comment'),
        ('dm', 'Direct Message'),
        ('post_like', 'Post Like'),
        ('comment_like', 'Comment Like'),
    ]
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key to link to any model (Post, Comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
