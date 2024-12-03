# forms.py
from django import forms
from .models import Action

class CreateTaskForm(forms.ModelForm):
    # Override fields for better presentation
    actions = forms.ChoiceField(
        choices=[('react', 'React'), ('comment', 'Comment'), ('share', 'Share')],
        required=True
    )
    action_description = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Action description"}), required=True)
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Task URL"}), required=True)
    reaction = forms.ChoiceField(
        choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry')],
        required=False
    )
    comment_text = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comment text"}), required=False
    )
    comment_tags = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comma-separated tags"}), required=False
    )
    caption = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Caption"}), required=False
    )
    caption_tags = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comma-separated tags"}), required=False
    )

    class Meta:
        model = Action
        fields = [
            'action_description', 'required_bot_count', 'actions', 'url',
            'reaction', 'comment_text', 'comment_tags', 'caption', 'caption_tags'
        ]
