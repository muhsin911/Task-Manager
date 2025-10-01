# Generic task detail view for all roles
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Task, UserProfile
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from .forms import TaskForm


# Task Detail View (generic)
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


# User Profile View
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile.html'

    def get_object(self):
        try:
            return self.request.user.userprofile
        except UserProfile.DoesNotExist:
            # Create a UserProfile if missing
            return UserProfile.objects.create(user=self.request.user)


# Permissions
class IsAuthenticatedAndUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='User').exists()
        )


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists()


# API Views
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedAndUser]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticatedAndUser]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status != 'Completed':
            instance.completion_report = None
            instance.worked_hours = None
            instance.save()


class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_object(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.status != 'Completed':
            raise PermissionDenied("Report only available for completed tasks.")
        return task


# User-facing: List their own tasks
class UserTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks_list_user.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


# User-facing: Update their own task
class UserTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['status', 'completion_report', 'worked_hours']
    template_name = 'task_update_user.html'
    success_url = reverse_lazy('tasks_list_user')

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def get_form(self, form_class=None):
        from django import forms

        class UserTaskForm(forms.ModelForm):
            class Meta:
                model = Task
                fields = ['status', 'completion_report', 'worked_hours']

        return UserTaskForm(**self.get_form_kwargs())

    def form_valid(self, form):
        if self.get_object().assigned_to != self.request.user:
            form.add_error(None, "You do not have permission to update this task.")
            return self.form_invalid(form)
        return super().form_valid(form)
