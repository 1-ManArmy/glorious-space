from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DeveloperProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create developer profile
            DeveloperProfile.objects.create(user=user)
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'github_username', 
                 'linkedin_profile', 'website', 'preferred_language']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'github_username': forms.TextInput(attrs={'placeholder': 'Enter your GitHub username'}),
            'linkedin_profile': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/your-profile'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
        }


class DeveloperProfileForm(forms.ModelForm):
    class Meta:
        model = DeveloperProfile
        fields = ['experience_level', 'specializations']
        widgets = {
            'specializations': forms.TextInput(attrs={
                'placeholder': 'e.g., React, Python, Machine Learning (comma-separated)'
            })
        }
