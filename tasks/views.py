from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegistrationForm, TaskForm
from .models import Task
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})
@login_required
def create_task(request):
    if not request.user.is_superuser:  #if the user is not a superuser
        user = request.user
    else:
        user = None   #for normal user

    if request.method == 'POST':
        form = TaskForm(request.POST)  #from the forms.py i.e taskform
        if form.is_valid():  #if the form 's data is proper then ssave
            task = form.save(commit=False)
            if not form.cleaned_data['user']:
                task.user = user  
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)   #retreive the id 

   
    if task.user != request.user and not request.user.is_superuser:     # The user must either be the task's assigned user or a superuser
        return HttpResponseForbidden("You do not have permission to edit this task.")

    if request.method == 'POST':  
        form = TaskForm(request.POST, instance=task)           #create the instance and update the existimg data
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})

def delete_task(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    task.delete()
    return redirect('task_list') 
@login_required
def complete_task(request, task_id):
 
        task = Task.objects.get(id=task_id,user=request.user)
        task.completed = True
        task.save()
        return redirect('task_list') 









