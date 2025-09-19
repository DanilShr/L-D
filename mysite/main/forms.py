from django import forms

from main.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'email', 'avatar')