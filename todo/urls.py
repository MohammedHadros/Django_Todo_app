from django.urls import path
from .views import index,create_todo,todo_detiles,todo_delete,todo_edit

urlpatterns = [
    path('',index ,name="Home"),
    path('create/',create_todo ,name="create-todo"),
    path('todo/<int:id>',todo_detiles ,name="todo-detiles"),
    path('todo-delete/<int:id>',todo_delete ,name="todo-delete"),
    path('todo-edit/<int:id>',todo_edit ,name="todo-edit"),

]