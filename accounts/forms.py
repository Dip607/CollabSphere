from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form for CollabSphere
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'role-select'})
    )
    passout_batch = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Graduation year (e.g., 2024)',
            'id': 'passout-batch-field'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'role', 'passout_batch')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        passout_batch = cleaned_data.get('passout_batch')
        
        # If role is professor, clear passout_batch
        if role == 'professor' and passout_batch:
            cleaned_data['passout_batch'] = ''
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.passout_batch = self.cleaned_data['passout_batch']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form using email instead of username
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password.')
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class ProfileCompletionForm(forms.ModelForm):
    """
    Form for completing user profile after first login
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'profile_pic')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile
    """
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    passout_batch = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Graduation year (e.g., 2024)',
            'id': 'passout-batch-field'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_pic', 'passout_batch')
    
    def clean(self):
        cleaned_data = super().clean()
        role = self.instance.role
        passout_batch = cleaned_data.get('passout_batch')
        
        # If role is professor, clear passout_batch
        if role == 'professor' and passout_batch:
            cleaned_data['passout_batch'] = ''
        
        return cleaned_data 