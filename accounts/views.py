from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileCompletionForm, ProfileEditForm
from .models import CustomUser, Notification


def signup(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('accounts:profile_completion')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view using email authentication
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.get_full_name()}!')
        
        # Check if user needs to complete profile
        if not self.request.user.username:
            return redirect('accounts:profile_completion')
        
        return response


def logout_view(request):
    """
    Logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_completion(request):
    """
    Profile completion view for new users
    """
    if request.user.username:
        messages.info(request, 'Your profile is already complete.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileCompletionForm(instance=request.user)
    
    return render(request, 'accounts/profile_completion.html', {'form': form})


@login_required
def dashboard(request):
    """
    User dashboard view
    """
    user = request.user
    context = {
        'user': user,
        'role_display': dict(CustomUser.ROLE_CHOICES)[user.role],
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_edit(request):
    """
    Profile editing view
    """
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
        'role_display': dict(CustomUser.ROLE_CHOICES)[request.user.role],
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def notifications(request):
    """View for user's notifications"""
    notifications_list = request.user.notifications.all()
    return render(request, 'accounts/notifications.html', {
        'notifications': notifications_list
    })


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})


@login_required
def get_unread_notifications_count(request):
    """Get count of unread notifications for AJAX"""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})
