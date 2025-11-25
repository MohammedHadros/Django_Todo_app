from django.test import TestCase
from authentication.models import User
from faker import Faker

class TestSetup(TestCase):
    def setUp(self):
        print("Test started")
        self.faker=Faker()
        self.password=self.faker.password()
        # print(self.faker.user_name())
        # print(self.faker.name().split(' ')[0])
        self.user={
            'username':self.faker.name().split(' ')[0],
            'email':self.faker.email(),
            'password':self.password,
            'conpassword':self.password
        }
        return super().setUp()
    
    def create_test_user(self):
        user=User.objects.create_user(
            username=self.faker.name().split(' ')[0] , 
            email=self.faker.email(),
            is_email_verified=True
            )
        user.set_password('password12!')
        user.save()
        return user
    
    def create_test_user_tow(self):
        user=User.objects.create_user(
            username="username2" , 
            email="email2@gmail.com"
            )
        user.set_password=('password12!')
        user.save()
        return user
    
    def tearDown(self):
        print("Test end")
        return super().tearDown()