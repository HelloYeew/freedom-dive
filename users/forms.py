from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ColourSettings, Profile


class UserCreationForms(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserCreationFromRequestForms(UserCreationForm):
    """Form for creating a new user from request."""
    class Meta:
        model = User
        fields = ['password1', 'password2']


class UserProfileForms(forms.ModelForm):
    """Form for updating user profile."""
    avatar = forms.ImageField(label='Profile Picture', widget=forms.FileInput(attrs={'class': 'form-control'}),
                                       help_text='Upload a new profile picture.', required=False)
    background = forms.ImageField(label='Background', widget=forms.FileInput(attrs={'class': 'form-control'}),
                                        help_text='Upload a new profile page background.', required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'background']


class ColourSettingsForm(forms.ModelForm):
    """User's styling settings for the homepage"""
    color_primary = forms.CharField(label="Primary color", widget=forms.TextInput(
        attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        help_text="A primary color of the site. This mainly use as text color.",
        max_length=255,
        initial='#DFD9D6'
    )
    color_accent = forms.CharField(label="Accent color", widget=forms.TextInput(
        attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        help_text="An accent color of the site. This color will be use as the theme's second color.",
        max_length=255,
        initial='#DBC2D1'
    )
    color_background = forms.CharField(label="Background color", widget=forms.TextInput(
        attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        help_text="A background color of the site. This color will be use anywhere on background element.",
        max_length=255,
        initial='#0A0A0A'
    )
    mask_opacity = forms.FloatField(label="Mask Opacity",
                                    help_text="A mask opacity of the mask between site's body and background",
                                    max_value=1, min_value=0, initial=0.5, step_size=0.01)

    class Meta:
        model = ColourSettings
        fields = ['color_primary', 'color_accent', 'color_background', 'mask_opacity']


class SiteSettingsForm(forms.ModelForm):
    """User's site settings"""
    use_traditional_metadata = forms.BooleanField(label="Use Traditional Metadata",
                                                  help_text="Use traditional metadata if available.",
                                                  required=False)

    class Meta:
        model = ColourSettings
        fields = ['use_traditional_metadata']