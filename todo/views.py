from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def get_showing_todos(request,todos):
    if request.GET and request.GET.get("filter"):
        if request.GET.get("filter")=="completed":
            todos=todos.filter(is_completed=True)
        elif request.GET.get("filter")=="remaining":
            todos=todos.filter(is_completed=False)
    return todos

@login_required
def index(request):
    todos=Todo.objects.filter(owner=request.user)
    completed=Todo.objects.filter(is_completed=True).count()
    remaining=Todo.objects.filter(is_completed=False).count()
    all=todos.count()
    context={
        "todos":get_showing_todos(request,todos),
        'completed':completed,
        'remaining':remaining,
        'all':all
        }
    return render(request,"todo/index.html",context)


                      
@login_required
def create_todo(request):
    form = TodoForm()
    # print(1)
    if request.method=="POST":
        form = TodoForm(request.POST)
        # print(2)
        title=request.POST.get("title")
        description=request.POST.get("description")
        is_completed=request.POST.get("is_completed",False)
        todo=Todo()
        todo.title=title
        todo.description=description
        todo.is_completed=True if is_completed=="on" else False
        todo.owner=request.user
        todo.save()
        messages.add_message(request ,messages.SUCCESS , "ToDo Has Been Created Sucssesfuly" )
        # print(3)
        return HttpResponseRedirect(reverse("todo-detiles", args=[todo.pk]))



    context={
        'form':form
    }
    return render(request,"todo/create_todo.html",context)



@login_required
def todo_detiles(request,id):
    todo=get_object_or_404(Todo,pk=id)
    context={'todo':todo}
    return render(request,"todo/todo_detiles.html",context)


@login_required
def todo_delete(request,id):
    todo=get_object_or_404(Todo,pk=id)
    context={'todo':todo}
    if request.method=='POST':
        if todo.owner==request.user:
            todo.delete()
            messages.add_message(request ,messages.WARNING , "ToDo Has Been Created Deleted" )

            return HttpResponseRedirect(reverse("Home"))
    return render(request,"todo/todo_delete.html",context)



@login_required
def todo_edit(request,id):
    todo=get_object_or_404(Todo,pk=id)
    form = TodoForm(instance=todo)
    context={'todo':todo , 'form':form}
    if request.method=='POST':
        if form.is_valid:
            todo.title=request.POST.get("title")
            todo.description=request.POST.get("description")
            todo.is_completed=True if request.POST.get("is_completed",False)=="on" else False
            if todo.owner==request.user:
                todo.save()
                messages.add_message(request ,messages.SUCCESS , "Modification completed" )

                return HttpResponseRedirect(reverse("todo-detiles", args=[todo.pk]))
    return render(request,"todo/todo_edit.html",context)

