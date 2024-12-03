from django import forms
from .models import Action

class CreateTaskForm(forms.ModelForm):
    actions = forms.ChoiceField(
        choices=[('react', 'React'), ('comment', 'Comment'), ('share', 'Share')],
        required=True
    )
    action_description = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Action description"}),
        required=True
    )
    urls = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter one URL per line"}),
        required=True
    )
    reaction = forms.ChoiceField(
        choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry')],
        required=False
    )
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Comment text"}),
        required=False
    )
    comment_tags = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comma-separated tags"}),
        required=False
    )
    caption = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Caption"}),
        required=False
    )
    caption_tags = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Comma-separated tags"}),
        required=False
    )
    
    def get_action_data(self):
        """Retrieve structured action data from form fields."""
        return {
            "actions": self.cleaned_data.get("actions"),
            "data": {
                "urls": [
                    url.strip() for url in self.cleaned_data.get("urls", "").splitlines() if url.strip()
                ],
                "reaction": self.cleaned_data.get("reaction"),
                "comment_text": self.cleaned_data.get("comment_text"),
                "comment_tags": [
                    tag.strip() for tag in self.cleaned_data.get("comment_tags", "").split(",") if tag.strip()
                ],
                "caption": self.cleaned_data.get("caption"),
                "caption_tags": [
                    tag.strip() for tag in self.cleaned_data.get("caption_tags", "").split(",") if tag.strip()
                ],
            },
        }

    class Meta:
        model = Action
        fields = [
            'action_description', 'required_bot_count', 'actions', 'urls',
            'reaction', 'comment_text', 'comment_tags', 'caption', 'caption_tags'
        ]
