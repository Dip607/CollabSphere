from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, Comment, DirectMessage
from .forms import PostForm, CommentForm, DirectMessageForm
from accounts.models import CustomUser, Notification
from django.contrib.contenttypes.models import ContentType

# community/views.py
# views.py


from .models import Mentorship

# community/views.py


from .models import AlumniStory
from .forms import AlumniStoryForm


@login_required
def alumni_story_list(request):
    stories = AlumniStory.objects.order_by('-created_at')
    return render(request, 'community/alumni_story_list.html', {'stories': stories})

@login_required
def alumni_stories_view(request):
    if request.user.role != 'student':
        return redirect('home')  # or show 403
    stories = AlumniStory.objects.all()
    return render(request, 'community/alumni_stories.html', {'stories': stories})
@login_required
def alumni_story_create(request):
    if request.user.role != 'alumni':
        return redirect('home')

    if request.method == 'POST':
        form = AlumniStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('community:alumni_stories')
    else:
        form = AlumniStoryForm()
    return render(request, 'community/alumni_story_form.html', {'form': form})



@login_required
def professor_student_list_view(request):
    if request.user.role == 'professor':
        mentorship = Mentorship.objects.filter(mentor=request.user).first()
        return render(request, 'community/professor_student_list.html', {'mentorship': mentorship})
    return render(request, 'community/access_denied.html')

@login_required
def student_mentor_view(request):
    mentorship = Mentorship.objects.filter(students=request.user).first()
    students = mentorship.students.exclude(id=request.user.id) if mentorship else []

    return render(request, 'community/student_mentor_view.html', {
        'mentorship': mentorship,
        'students': students,
    })

@login_required
def post_list(request):
    """
    View to display all posts with pagination
    """
    posts = Post.objects.all()
    
    # Filter by post type if specified
    post_type = request.GET.get('type')
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'post_types': Post.POST_TYPE_CHOICES,
        'current_filter': post_type,
    }
    return render(request, 'community/post_list.html', context)


@login_required
def post_create(request):
    """
    View to create a new post
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('community:post_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'post_types': Post.POST_TYPE_CHOICES,
    }
    return render(request, 'community/post_create.html', context)


@login_required
def post_detail(request, pk):
    """
    View to display a single post
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            # Create notification for post author (if not commenting on own post)
            if comment.user != post.created_by:
                Notification.objects.create(
                    recipient=post.created_by,
                    notification_type='comment',
                    title=f'New comment on your post "{post.title}"',
                    message=f'{comment.user.get_full_name()} commented on your post: "{comment.content[:50]}{"..." if len(comment.content) > 50 else ""}',
                    content_type=ContentType.objects.get_for_model(Comment),
                    object_id=comment.id
                )
            
            messages.success(request, 'Comment added successfully!')
            return redirect('community:post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'community/post_detail.html', context)


@login_required
def post_edit(request, pk):
    """
    View to edit an existing post (only by the creator)
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the creator of the post
    if post.created_by != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('community:post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('community:post_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'post_types': Post.POST_TYPE_CHOICES,
    }
    return render(request, 'community/post_edit.html', context)


@login_required
def post_delete(request, pk):
    """
    View to delete a post (only by the creator)
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the creator of the post
    if post.created_by != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('community:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community:post_list')
    
    context = {
        'post': post,
    }
    return render(request, 'community/post_delete.html', context)


@login_required
def inbox(request):
    """View for user's message inbox"""
    # Get all conversations for the current user
    conversations = DirectMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values('sender', 'recipient').distinct()
    
    # Create a list of unique conversation partners
    conversation_partners = []
    for conv in conversations:
        if conv['sender'] == request.user.id:
            partner_id = conv['recipient']
        else:
            partner_id = conv['sender']
        
        partner = CustomUser.objects.get(id=partner_id)
        unread_count = DirectMessage.objects.filter(
            sender=partner, recipient=request.user, is_read=False
        ).count()
        
        # Get the latest message
        latest_message = DirectMessage.objects.filter(
            Q(sender=request.user, recipient=partner) | 
            Q(sender=partner, recipient=request.user)
        ).order_by('-created_at').first()
        
        conversation_partners.append({
            'partner': partner,
            'unread_count': unread_count,
            'latest_message': latest_message
        })
    
    # Sort by latest message
    conversation_partners.sort(key=lambda x: x['latest_message'].created_at if x['latest_message'] else x['partner'].date_joined, reverse=True)
    
    return render(request, 'community/inbox.html', {
        'conversation_partners': conversation_partners
    })


@login_required
def conversation(request, user_id):
    """View for a specific conversation between two users"""
    other_user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_user
            message.save()
            
            # Create notification for recipient
            Notification.objects.create(
                recipient=other_user,
                notification_type='dm',
                title=f'New message from {request.user.get_full_name()}',
                message=f'You have a new message from {request.user.get_full_name()}',
                content_type=ContentType.objects.get_for_model(DirectMessage),
                object_id=message.id
            )
            
            return redirect('community:conversation', user_id=user_id)
    else:
        form = DirectMessageForm()
    
    # Get conversation messages
    messages_list = DirectMessage.get_conversation(request.user, other_user)
    
    # Mark messages as read
    DirectMessage.objects.filter(
        sender=other_user, recipient=request.user, is_read=False
    ).update(is_read=True)
    
    return render(request, 'community/conversation.html', {
        'other_user': other_user,
        'messages': messages_list,
        'form': form
    })


@login_required
def send_message(request, user_id):
    """AJAX view for sending messages"""
    if request.method == 'POST':
        recipient = get_object_or_404(CustomUser, id=user_id)
        form = DirectMessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            
            # Create notification for recipient
            Notification.objects.create(
                recipient=recipient,
                notification_type='dm',
                title=f'New message from {request.user.get_full_name()}',
                message=f'You have a new message from {request.user.get_full_name()}',
                content_type=ContentType.objects.get_for_model(DirectMessage),
                object_id=message.id
            )
            
            return JsonResponse({
                'success': True,
                'message': message.message,
                'created_at': message.created_at.strftime('%H:%M'),
                'sender_name': request.user.get_full_name()
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
