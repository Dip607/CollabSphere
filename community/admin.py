from django.contrib import admin
from .models import Post
# community/admin.py
from .models import Mentorship

class MentorshipAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'created_at')
    filter_horizontal = ('students',)

admin.site.register(Mentorship, MentorshipAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'created_by', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('title', 'content', 'created_by__email', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
