from django import forms
from django.contrib.auth.models import User
from .models import Task


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)  

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'user']  
