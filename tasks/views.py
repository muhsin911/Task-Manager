from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Task, UserProfile
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class IsAuthenticatedAndUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='User').exists()

class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists()

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

# User Profile View
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile.html'

    def get_object(self):
        return self.request.user.userprofile