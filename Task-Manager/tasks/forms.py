from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Task, UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_report': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if queryset:
            self.fields['assigned_to'].queryset = queryset

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completion_report = cleaned_data.get('completion_report')
        worked_hours = cleaned_data.get('worked_hours')
        if status == 'Completed' and (not completion_report or not worked_hours):
            raise forms.ValidationError("Completion report and worked hours are required for completed tasks.")
        if status != 'Completed':
            cleaned_data['completion_report'] = None
            cleaned_data['worked_hours'] = None
        return cleaned_data


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class AdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AssignUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='User'))
    admin = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Admin'))