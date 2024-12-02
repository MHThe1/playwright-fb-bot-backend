from django import forms
from .models import Action

class CreateTaskForm(forms.ModelForm):
    actions = forms.MultipleChoiceField(
        choices=[('react', 'React'), ('comment', 'Comment'), ('share', 'Share')],
        widget=forms.CheckboxSelectMultiple,
        label="Actions"
    )
    action_description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter task description'}),
        label="Task Description"
    )
    profile_switch_option = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        required=True,
        label="Profile Switch Option"
    )
    url = forms.URLField(label="Post URL", required=True)
    reaction = forms.ChoiceField(
        choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('haha', 'Haha'), ('sad', 'Sad'), ('angry', 'Angry')],
        required=False,
        label="Reaction"
    )
    comment_text = forms.CharField(widget=forms.TextInput, required=False, label="Comment Text")
    comment_tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        required=False,
        label="Comment Tags"
    )
    caption = forms.CharField(widget=forms.TextInput, required=False, label="Caption")
    caption_tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        required=False,
        label="Caption Tags"
    )

    class Meta:
        model = Action
        fields = ['action_description', 'required_bot_count']
        labels = {
            'action_description': 'Task Description',
            'required_bot_count': 'Number of Required Bots',
        }

    def clean(self):
        """
        Custom clean method to validate and format JSON data.
        """
        cleaned_data = super().clean()
        comment_tags = cleaned_data.get('comment_tags', '')
        caption_tags = cleaned_data.get('caption_tags', '')

        # Convert comma-separated tags into a list
        cleaned_data['comment_tags'] = [tag.strip() for tag in comment_tags.split(',') if tag.strip()]
        cleaned_data['caption_tags'] = [tag.strip() for tag in caption_tags.split(',') if tag.strip()]
        return cleaned_data

    def get_action_data(self):
        """
        Combine fields into a JSON structure for the action_data field.
        """
        return {
            "actions": self.cleaned_data['actions'],
            "profile_switch_option": self.cleaned_data['profile_switch_option'],
            "data": {
                "url": self.cleaned_data['url'],
                "reaction": self.cleaned_data['reaction'],
                "comment_text": self.cleaned_data['comment_text'],
                "comment_tags": self.cleaned_data['comment_tags'],
                "caption": self.cleaned_data['caption'],
                "caption_tags": self.cleaned_data['caption_tags'],
            }
        }
