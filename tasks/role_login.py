from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='SuperAdmin').exists():
            return reverse('user_list')
        elif user.groups.filter(name='Admin').exists():
            return reverse('task_list_admin')
        elif user.groups.filter(name='User').exists():
            return reverse('profile')
        return super().get_success_url()
