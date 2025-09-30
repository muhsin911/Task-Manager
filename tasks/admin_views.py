from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404, render
from django.core.exceptions import PermissionDenied
from .models import Task, UserProfile
from .forms import TaskForm, UserForm, AdminForm, AssignUserForm

# Permission Mixins
class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='SuperAdmin').exists()

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists()

# User Management (SuperAdmin Only)
class UserListView(SuperAdminRequiredMixin, ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        # If user is Admin (not SuperAdmin), redirect to /admin/tasks/
        if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
            return redirect('task_list_admin')
        return super().dispatch(request, *args, **kwargs)

class UserCreateView(SuperAdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign default 'User' group
        user_group = Group.objects.get(name='User')
        self.object.groups.add(user_group)
        return response

class UserUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

# Admin Management (SuperAdmin Only)
class AdminListView(SuperAdminRequiredMixin, ListView):
    model = User
    template_name = 'admins_list.html'
    context_object_name = 'admins'

    def get_queryset(self):
        return User.objects.filter(groups__name='Admin')

class AdminCreateView(SuperAdminRequiredMixin, CreateView):
    model = User
    form_class = AdminForm
    template_name = 'admin_form.html'
    success_url = reverse_lazy('admin_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        admin_group = Group.objects.get(name='Admin')
        self.object.groups.add(admin_group)
        return response

class AdminUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = User
    form_class = AdminForm
    template_name = 'admin_form.html'
    success_url = reverse_lazy('admin_list')

class AdminDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'admin_confirm_delete.html'
    success_url = reverse_lazy('admin_list')

# Task Management (Admin and SuperAdmin)
class TaskListAdminView(AdminRequiredMixin, ListView):
    model = Task
    template_name = 'tasks_list_admin.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.groups.filter(name='SuperAdmin').exists():
            return Task.objects.all()
        # Admins see tasks of users they manage
        return Task.objects.filter(assigned_to__userprofile__managed_by=self.request.user)

class TaskCreateView(AdminRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list_admin')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not self.request.user.groups.filter(name='SuperAdmin').exists():
            # Limit assigned_to choices to users managed by this admin
            kwargs['queryset'] = User.objects.filter(userprofile__managed_by=self.request.user)
        return kwargs

class TaskUpdateView(AdminRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list_admin')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not self.request.user.groups.filter(name='SuperAdmin').exists():
            kwargs['queryset'] = User.objects.filter(userprofile__managed_by=self.request.user)
        return kwargs

class TaskDeleteView(AdminRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list_admin')

class TaskReportDetailView(AdminRequiredMixin, DetailView):
    model = Task
    template_name = 'task_report.html'
    context_object_name = 'task'

    def get_object(self):
        task = super().get_object()
        if task.status != 'Completed':
            raise PermissionDenied("Report only available for completed tasks.")
        return task

# Custom View: Assign Users to Admins (SuperAdmin Only)
class AssignUserToAdminView(SuperAdminRequiredMixin, View):
    template_name = 'assign_user_form.html'

    def get(self, request, *args, **kwargs):
        form = AssignUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AssignUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            admin = form.cleaned_data['admin']
            user.userprofile.managed_by.add(admin)
            return redirect('user_list')
        return render(request, self.template_name, {'form': form})

# Custom View: Promote/Demote Admins (SuperAdmin Only)
class AdminPromoteDemoteView(SuperAdminRequiredMixin, View):
    def post(self, request, pk, action):
        user = get_object_or_404(User, pk=pk)
        admin_group = Group.objects.get(name='Admin')
        user_group = Group.objects.get(name='User')
        if action == 'promote':
            user.groups.remove(user_group)
            user.groups.add(admin_group)
        elif action == 'demote':
            user.groups.remove(admin_group)
            user.groups.add(user_group)
        return redirect('admin_list')