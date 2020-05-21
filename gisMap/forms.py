from django import forms
from .models import ImagePoint

class ImagePointForm(forms.ModelForm):
    class Meta:
        model = ImagePoint
        fields = ['description', 'image']

