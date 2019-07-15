from django.contrib.auth.models import User
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

    def test_contact_form_is_valid_with_correct_data(self):
        """
        Check if form accepts correct data
        """
        self.assertTrue(self.correct_form.is_valid())

    def test_send_email_throws_exception_if_no_superusers(self):
        """
        Check if no superusers error is handled
        """
        self.correct_form.send_email("testusername")
        self.assertRaises(ValueError)

    def test_send_email_throws_exception_if_superusers_have_no_emails(self):
        """
        Check if no superuser emails erro is handled
        """
        superuser = User.objects.create_user(username='test_superuser')
        superuser.is_staff = True
        self.client.force_login(superuser)

        self.correct_form.send_email("testusername")
        self.assertRaises(ValueError)
