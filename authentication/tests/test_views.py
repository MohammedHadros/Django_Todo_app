from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
import pdb
from utils.set_up_test import TestSetup

class TestViews(TestSetup):

    def test_should_show_regester_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"authentication/register.html")


    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"authentication/login.html")

    def test_should_signup_user(self):
        response=self.client.post(reverse('register' ), self.user)
        self.assertEqual(response.status_code,302)#redirected status code


    def test_should_not_signup_user_with_tacken_username(self):

        self.client.post(reverse('register') , self.user)
        response=self.client.post(reverse('register') , self.user)
        self.assertEqual(response.status_code,409)#created status code
        storage=get_messages(response.wsgi_request)
        # error=[]
        # for message in storage:
        #     print(message)
        #     error.append(message.message)
        # print(error)
        # self.assertIn("username is Tacken, Please enter another username" , error)
        # pdb.set_trace()
        self.assertIn("username is Tacken, Please enter another username" ,
            list(map(lambda x:x.message , storage)))



    def test_should_not_signup_user_with_tacken_email(self):
        self.user={
            'username':'username1',
            'email':'email12@gamil.com',
            'password':'password',
            'conpassword':'password'
        }
        self.user2={
            'username':'username11',
            'email':'email12@gamil.com',
            'password':'password',
            'conpassword':'password'
        }
        self.client.post(reverse('register') , self.user)
        response=self.client.post(reverse('register') , self.user2)
        self.assertEqual(response.status_code,419)#created status code


    def test_should_login_successfully(self):
        user=self.create_test_user()
        response=self.client.post(reverse('login') , {
            'username':user.username,
            'password':"password12!"
        })
        self.assertEqual(response.status_code,302)
        storage=get_messages(response.wsgi_request)
        self.assertIn(f"Welcome {user.username}" ,
            list(map(lambda x:x.message , storage)))
        # self.assertEqual(f"Welcome {user.}")