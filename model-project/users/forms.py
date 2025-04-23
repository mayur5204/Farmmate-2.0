from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'phone_number', 
                 'farmer_type', 'farming_experience', 'preferred_crops', 'farm_size']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'farmer_type': forms.Select(attrs={'class': 'form-control'}),
            'farming_experience': forms.Select(attrs={'class': 'form-control'}),
            'preferred_crops': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rice, Wheat, Maize (comma separated)'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProfilePictureForm(forms.ModelForm):
    """Separate form for handling only profile picture updates"""
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
                'id': 'profile-pic-input'
            })
        }
        
    def clean_profile_picture(self):
        """Validate that the uploaded file is an image and not too large"""
        image = self.cleaned_data.get('profile_picture', False)
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large (maximum 5MB)")
            return image
        return image

class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with bootstrap styling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Current password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm new password'})