from django.test import TestCase
from authentication.models import User
from todo.models import Todo
from utils.set_up_test import TestSetup
from django.urls import reverse

class TestModel(TestSetup):
    def test_should_create_todo(self):
        user=self.create_test_user()
        # Log in the user
        self.client.post(reverse('login') , {
            'username':user.username,
            'password':"password12!"
        })
        print('//////////////////////////////')
        todos=Todo.objects.all()
        self.assertEqual(todos.count(),0)
        response=self.client.post(reverse('create-todo'),{
            'owner':user,
            'title':"Hello",
            "description":'Remember to pray'
        })
        print(response)
        updated_todos=Todo.objects.all()
        self.assertEqual(updated_todos.count(),1)
        self.assertEqual(response.status_code,302)