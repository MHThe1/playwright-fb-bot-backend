from rest_framework import serializers
from .models import Action

class ActionSerializer(serializers.ModelSerializer):
    bot_count = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = [
            'id',
            'action_description',
            'action_data',
            'created_at',
            'completed_by',
            'bot_count',
            'assigned_to',
            'is_assigning',
            'is_complete',
            'required_bot_count',
        ]

    def get_bot_count(self, obj):
        return len(obj.completed_by)
