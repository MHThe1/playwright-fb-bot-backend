from django.db import models

class Action(models.Model):
    action_description = models.TextField()
    action_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_by = models.JSONField(default=list)  # Tracks bots that completed the task
    assigned_to = models.JSONField(default=list)  # Tracks bots assigned to the task
    is_assigning = models.BooleanField(default=True)  # Indicates if assignment is in progress
    is_complete = models.BooleanField(default=False)  # Changes to true when required bots complete the task
    required_bot_count = models.PositiveIntegerField(default=5)  # Threshold for task completion

    def __str__(self):
        return f"Action created at {self.created_at}"

    def update_completion_status(self):
        """
        Updates is_complete status based on completed_by length.
        """
        if len(self.completed_by) >= self.required_bot_count:
            self.is_complete = True
        else:
            self.is_complete = False
            
        """
        Updates is_assigning status based on assigned_to length.
        """
        if len(self.assigned_to) >= self.required_bot_count:
            self.is_assigning = False
        else:    
            self.is_assigning = True
        self.save()
