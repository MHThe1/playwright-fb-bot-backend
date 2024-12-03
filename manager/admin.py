from django import forms
from django.contrib import admin
from .models import Action
import json

class ActionAdminForm(forms.ModelForm):
    # Unpack action_data fields
    actions = forms.ChoiceField(
        choices=[("react", "React"), ("comment", "Comment"), ("share", "Share")],
        required=False,
        label="Actions"
    )
    urls = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter one URL per line"}), 
        required=False, 
        label="Task URLs"
    )
    reaction = forms.ChoiceField(
        choices=[("like", "Like"), ("love", "Love"), ("haha", "Haha"), ("sad", "Sad"), ("angry", "Angry")],
        required=False,
        label="Reaction"
    )
    comment_text = forms.CharField(required=False, label="Comment text")
    comment_tags = forms.CharField(required=False, label="Comment tags (comma-separated)")
    caption = forms.CharField(required=False, label="Caption")
    caption_tags = forms.CharField(required=False, label="Caption tags (comma-separated)")

    class Meta:
        model = Action
        fields = ["action_description", "required_bot_count", "actions", "urls", "reaction", 
                  "comment_text", "comment_tags", "caption", "caption_tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill form fields with unpacked data
        if self.instance and self.instance.action_data:
            data = self.instance.action_data.get("data", {})
            self.fields["actions"].initial = self.instance.action_data.get("actions")
            self.fields["urls"].initial = "\n".join(data.get("urls", []))
            self.fields["reaction"].initial = data.get("reaction")
            self.fields["comment_text"].initial = data.get("comment_text")
            self.fields["comment_tags"].initial = ", ".join(data.get("comment_tags", []))
            self.fields["caption"].initial = data.get("caption")
            self.fields["caption_tags"].initial = ", ".join(data.get("caption_tags", []))

    def clean(self):
        cleaned_data = super().clean()
        urls_input = cleaned_data.get("urls", "")
        urls_list = [url.strip() for url in urls_input.splitlines() if url.strip()]

        # Pack data into JSON format
        cleaned_data["action_data"] = {
            "actions": cleaned_data.pop("actions"),
            "data": {
                "urls": urls_list,
                "reaction": cleaned_data.pop("reaction"),
                "comment_text": cleaned_data.pop("comment_text"),
                "comment_tags": [
                    tag.strip() for tag in cleaned_data.pop("comment_tags", "").split(",") if tag.strip()
                ],
                "caption": cleaned_data.pop("caption"),
                "caption_tags": [
                    tag.strip() for tag in cleaned_data.pop("caption_tags", "").split(",") if tag.strip()
                ],
            }
        }
        return cleaned_data


    def save(self, commit=True):
        # Update action_data before saving the instance
        self.instance.action_data = self.cleaned_data["action_data"]
        return super().save(commit)

# Admin Registration
class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm
    list_display = ("action_description", "required_bot_count", "is_complete")

admin.site.register(Action, ActionAdmin)
