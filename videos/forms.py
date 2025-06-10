from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'description',
            'author',
            'category',
            'tags',
            'youtube_url',
            'duration',
            'age',
            'year',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'Разделяй теги запятыми'}),
        }
