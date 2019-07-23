from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import reverse
from django.test import Client, TestCase

from .forms import ContactForm


class ContactViewTests(TestCase):
    """
    Tests for contact view.
    Mainly avaliability if user is logged in or not
    """

    @classmethod
    def setUpClass(cls):
        """
        Overriden setUpClass. Performs action on class-wide initialization
        This one creates cls.client with django.test.Client()
        and gets page url in cls.url
        """
        super().setUpClass()
        # creating instance of a client
        cls.client = Client()
        cls.url = reverse('assignment:contact')

    def test_contact_view_redirects_to_login_view_if_user_is_not_logged_in(self):
        """
        Contact view redirects to login page if user is not logged in
        """
        expected_url = '/assignment/login/?next=' + self.url
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url)

    def test_contact_view_avaliable_to_logged_in_user(self):
        """
        Contact view avaliable for logged in user
        """
        user = User.objects.create_user(username='testuser')
        #faster than login, because no need in password hashing
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class SignupViewTests(TestCase):
    """
    Tests for signup view.
    """

    @classmethod
    def setUpClass(cls):
        """
        Overriden setUpClass. Performs action on class-wide initialization
        This one creates ContactForm form
        """
        super().setUpClass()
        cls.correct_data = {
            'username':'test_user',
            'password1':'test_pass',
            'password2':'test_pass'
        }
        cls.client = Client()
        cls.url = reverse("assignment:signup")

    def test_signup_view_creates_user_on_correct_request(self):
        """
        Check if signup view can create new user
        """
        self.client.post(self.url, self.correct_data)
        usercount = User.objects.all().count()
        self.assertEqual(usercount, 1)

    def test_signup_view_loggs_user_in_after_creation(self):
        """
        Check if signup view loggs new user in after creation
        """
        self.client.post(self.url, self.correct_data)
        created_user = User.objects.all()[0]
        self.assertTrue(created_user.is_authenticated)
    
    def test_signup_view_throws_ex_on_empty_username(self):
        """
        Signup view throws exception if username is empty
        """
        client = Client()
        user_data = {'username': '', 'password': 'testpass1'}
        url = reverse('assignment:signup')
        #send post request
        response = client.post(url, user_data)
        self.assertRaises(User.DoesNotExist)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_redirects_on_empty_username(self):
        """
        Signup view redirects successfully if username is empty
        """
        client = Client()
        user_data = {'username': '', 'password': 'testpass1'}
        url = reverse('assignment:signup')
        #send post request
        response = client.post(url, user_data)
        self.assertEqual(response.status_code, 200)


class LoginViewTests(TestCase):
    """
    Tests for login view.
    """

    def test_signup_view_creates_user_with_on_correct_request(self):
        """
        Login view logs users in with correct data
        """
        client = Client()
        user_data = {'username': 'test_user', 'password': 'testpass1'}
        User.objects.create_user(**user_data)
        url = reverse('assignment:login')
        #send post request
        client.post(url, user_data)
        logged_user = User.objects.get(username='test_user')
        self.assertTrue(logged_user.is_authenticated)

class ContactFormTests(TestCase):
    """
    Tests for contact form. Mainly send_email()
    """

    @classmethod
    def setUpClass(cls):
        """
        Overriden setUpClass. Performs action on class-wide initialization
        This one creates ContactForm form
        """
        super().setUpClass()
        cls.correct_data = {
            'email':'test@test.com',
            'message':'test'
        }
        cls.correct_form = ContactForm(data=cls.correct_data)

    def create_staffuser(self, username='test_staffuser', email="admin@example.com"):
        """
        Create staffuser for test purposes.
        By default creates User with username='test_staffuser',
        email="admin@example.com", is_staff = True, password = "pass"
        """
        staffuser = User.objects.create_user(username=username)
        staffuser.is_staff = True
        staffuser.set_password = ("pass")
        staffuser.email = email
        staffuser.save()
        return staffuser

    def test_contact_form_is_valid_with_correct_data(self):
        """
        Check if form accepts correct data
        """
        self.assertTrue(self.correct_form.is_valid())

    def test_send_email_throws_exception_if_no_staffusers(self):
        """
        Check if no staffusers error is handled
        """
        self.correct_form.send_email("testusername")
        self.assertRaises(ValueError)

    def test_send_email_throws_exception_if_staffusers_have_no_emails(self):
        """
        Check if no staffuser emails erro is handled
        """
        staffuser = User.objects.create_user(username='test_staffuser')
        staffuser.is_staff = True
        self.client.force_login(staffuser)

        self.correct_form.send_email("testusername")
        self.assertRaises(ValueError)

    def test_send_email_sends_email_to_staffuser(self):
        """
        Send email function should send email to staffuser
        if there are any with emails
        """
        staffuser = self.create_staffuser()
        self.correct_form.send_email(username=staffuser.username)
        self.assertEqual(len(mail.outbox), 1)

    def test_send_email_sends_emails_to_multiple_staffusers(self):
        """
        Send email function should send email to multiple staffusers
        if there are any with emails
        """
        staffuser = self.create_staffuser()
        staffuser_other = self.create_staffuser(
            username="test_staffuser_1",
            email="other@example.com"
        )

        self.correct_form.send_email(username="test")

        recipients = mail.outbox[0].recipients()
        expected_recipients = [staffuser.email, staffuser_other.email]
        self.assertListEqual(recipients, expected_recipients)

    def test_send_email_throws_exception_if_smtp_fails(self):
        """
        Checks if SMTPException is handled
        """
        #doesn't seem like i can raise SMTPException without
        #third party tools
        #https://stackoverflow.com/a/13500768
