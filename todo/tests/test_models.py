from django.test import TestCase
from authentication.models import User
from todo.models import Todo
from utils.set_up_test import TestSetup

class TestModel(TestSetup):
    def test_should_create_user(self):
        user=self.create_test_user()
        todo=Todo(title="Comprer Pan",
                  description='muy importante',
                  is_completed=False,
                  owner=user)
        todo.save()
        self.assertEqual(str(todo),"Comprer Pan")