from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Action
from .serializers import ActionSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .forms import CreateTaskForm

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    
    @action(detail=False, methods=['post'])
    def create_task(self, request):
        """
        Creates a new task from the dashboard and returns the created task details.
        """
        try:
            # Deserialize the incoming data
            serializer = ActionSerializer(data=request.data)

            if serializer.is_valid():
                # Save the new task
                task = serializer.save()
                
                # Return the response with task details
                return Response({
                    "message": "Task created successfully.",
                    "action_id": task.id,
                    "action_title": task.action_description,
                    "action_data": task.action_data
                }, status=status.HTTP_201_CREATED)
            
            # If the serializer is not valid, return the errors
            return Response({
                "message": "Failed to create task.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": f"An error occurred: {str(e)}",
                "action_id": None,
                "action_title": None,
                "action_data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
    @action(detail=False, methods=['post'])
    def assign_bot(self, request):
        """
        Assigns a bot to the first eligible task where it is not already assigned or completed, 
        and returns the task details.
        """
        try:
            bot_id = request.data.get('bot_id')

            if bot_id is None:
                return Response({
                    "message": "bot_id is required.",
                    "action_id": None,
                    "action_title": None,
                    "action_data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Filter tasks where is_complete=False and is_assigning=True
            eligible_tasks = Action.objects.filter(is_complete=False, is_assigning=True).order_by('created_at')

            # Iterate through tasks to find the first assignable one
            for task in eligible_tasks:
                if bot_id not in task.assigned_to and bot_id not in task.completed_by:
                    # Assign the bot to the task
                    task.assigned_to.append(bot_id)
                    task.update_completion_status()

                    return Response({
                        "message": "Bot assigned successfully.",
                        "action_id": task.id,
                        "action_title": task.action_description,
                        "action_data": task.action_data
                    }, status=status.HTTP_200_OK)

            # If no assignable task is found
            return Response({
                "message": "No eligible tasks available.",
                "action_id": None,
                "action_title": None,
                "action_data": {}
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": f"An error occurred: {str(e)}",
                "action_id": None,
                "action_title": None,
                "action_data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    @action(detail=False, methods=['post'])
    def report_failure(self, request):
        """
        Removes a bot from the assigned_to list of a task when it fails to complete the task.
        """
        try:
            bot_id = request.data.get('bot_id')
            action_id = request.data.get('action_id')

            if not bot_id or not action_id:
                return Response({
                    "message": "Both bot_id and action_id are required.",
                    "action_id": action_id,
                    "action_data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the task by ID
            try:
                task = Action.objects.get(id=action_id)
            except Action.DoesNotExist:
                return Response({
                    "message": "Task not found.",
                    "action_id": action_id,
                    "action_data": {}
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the bot is in the assigned_to list
            if bot_id in task.assigned_to:
                # Remove the bot from the list
                task.assigned_to.remove(bot_id)
                task.save()

                return Response({
                    "message": "Bot removed from the assigned task.",
                    "action_id": task.id,
                    "action_title": task.action_description,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Bot is not assigned to this task.",
                    "action_id": task.id,
                    "action_data": task.action_data
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": f"An error occurred: {str(e)}",
                "action_id": None,
                "action_data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            
    @action(detail=False, methods=['post'])
    def complete_task(self, request):
        """
        Marks a task as complete after a bot finishes it, 
        by appending the bot's ID to the completed_by list.
        """
        try:
            bot_id = request.data.get('bot_id')
            action_id = request.data.get('action_id')

            if bot_id is None or action_id is None:
                return Response({
                    "message": "Both bot_id and action_id are required.",
                    "action_id": None,
                    "action_title": None,
                    "action_data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Find the action based on action_id
            task = Action.objects.filter(id=action_id).first()

            if not task:
                return Response({
                    "message": "Task not found.",
                    "action_id": None,
                    "action_title": None,
                    "action_data": {}
                }, status=status.HTTP_404_NOT_FOUND)

            if bot_id in task.completed_by:
                return Response({
                    "message": "This bot has already completed the task.",
                    "action_id": task.id,
                    "action_title": task.action_description,
                    "action_data": task.action_data
                }, status=status.HTTP_400_BAD_REQUEST)

            # Append bot_id to completed_by list
            task.completed_by.append(bot_id)
            task.update_completion_status()  # Update the task's completion status

            return Response({
                "message": "Task marked as complete by the bot.",
                "action_id": task.id,
                "action_title": task.action_description,
                "action_data": task.action_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": f"An error occurred: {str(e)}",
                "action_id": None,
                "action_title": None,
                "action_data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def create_task_form(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            # Construct the JSON structure
            action_data = form.get_action_data()

            # Save the task
            action = Action(
                action_description=form.cleaned_data['action_description'],
                required_bot_count=form.cleaned_data['required_bot_count'],
                action_data=action_data
            )
            action.save()

            return Response({
                "message": "Task created successfully.",
                "task_data": action_data
            }, status=201)
        else:
            return render(request, 'create_task_form.html', {'form': form})
    else:
        form = CreateTaskForm()
        return render(request, 'create_task_form.html', {'form': form})