from django.urls import path, include
from django.contrib.auth.views import LogoutView
from tasks.role_login import RoleBasedLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks.views import TaskListView, TaskUpdateView, TaskReportView, UserProfileView, UserTaskListView, UserTaskUpdateView, TaskDetailView
from tasks.admin_views import (
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    AdminListView, AdminCreateView, AdminUpdateView, AdminDeleteView,
    TaskListAdminView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskReportDetailView,
    AssignUserToAdminView, AdminPromoteDemoteView
)
from django.contrib import admin

urlpatterns = [
    # Home Page
    path('', lambda request: __import__('django').shortcuts.render(request, 'index.html'), name='home'),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    # User-facing task list and update
    path('my-tasks/', UserTaskListView.as_view(), name='tasks_list_user'),
    path('my-tasks/<int:pk>/update/', UserTaskUpdateView.as_view(), name='task_update_user'),
    path('tasks/<int:pk>/view/', TaskDetailView.as_view(), name='task_detail'),
    # API Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task_report'),
    # Admin Panel
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/users/create/', UserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('admin/admins/', AdminListView.as_view(), name='admin_list'),
    path('admin/admins/create/', AdminCreateView.as_view(), name='admin_create'),
    path('admin/admins/<int:pk>/update/', AdminUpdateView.as_view(), name='admin_update'),
    path('admin/admins/<int:pk>/delete/', AdminDeleteView.as_view(), name='admin_delete'),
    path('admin/admins/<int:pk>/<str:action>/', AdminPromoteDemoteView.as_view(), name='admin_promote_demote'),
    path('admin/users/assign/', AssignUserToAdminView.as_view(), name='assign_user'),
    path('admin/tasks/', TaskListAdminView.as_view(), name='task_list_admin'),
    path('admin/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('admin/tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('admin/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('admin/tasks/<int:pk>/report/', TaskReportDetailView.as_view(), name='task_report_detail'),
    # Login
    path('accounts/login/', RoleBasedLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    # Django Admin Site (must be last)
    path('admin/', admin.site.urls),
]