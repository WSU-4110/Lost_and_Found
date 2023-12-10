from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.core import mail
import random
from main.forms import RegisterForm
from unittest.mock import patch




class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_view_get_request(self):
        # Test GET request (should render the signup form)
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    # @patch('main.views.random.randint')
    # def test_signup_post_with_valid_data(self, mock_randint):
    #     mock_randint.return_value = 123456  # Mocked OTP

    #     valid_data = {
    #         'username': 'testuser1',
    #         'email': 'testuser@wayne.edu',  # Adjust this as per your form's requirements
    #         'password1': 'TestPassword123',
    #         'password2': 'TestPassword123',
    #         # Include any other fields required by your form
    #     }

    #     response = self.client.post(self.signup_url, valid_data)

    #     # Check if the user is created and redirected to OTP verification
    #     self.assertTrue(User.objects.filter(username='testuser').exists())
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('otp_verification'))  # Assuming 'otp_verification' is your OTP verification URL name

    #     # Optionally, check if the OTP is correctly stored in session
    #     self.assertEqual(self.client.session['otp'], 123456)

    def test_signup_post_with_invalid_data(self):
        # Test POST request with invalid data
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'This field is required.')


class OTPVerificationViewTest(TestCase):

    def setUp(self):
        # Create a user but don't save to the database yet
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'test@example.com'
        }
        self.user = User(**self.credentials)
        self.otp = '123456'
        self.client = Client()

        # Simulate session data for OTP verification
        session = self.client.session
        session['otp'] = self.otp
        session['username'] = self.credentials['username']
        session['email'] = self.credentials['email']
        session['password'] = self.credentials['password']
        session['otp_time'] = str(datetime.datetime.now())
        session.save()

    def test_otp_verification_success(self):
        # Test OTP verification with correct OTP and not expired
        response = self.client.post(reverse('otp_verification'), {'otp': self.otp})
        self.assertRedirects(response, reverse('list_report'))
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists())

    def test_otp_verification_expired(self):
    # Test OTP verification with correct OTP but expired
        session = self.client.session
        session['otp_time'] = str(datetime.datetime.now() - datetime.timedelta(minutes=3))
        session.save()
    
        response = self.client.post(reverse('otp_verification'), {'otp': self.otp})

        # Check that the user is not created
        self.assertFalse(User.objects.filter(username=self.credentials['username']).exists())

        # Check if the response is a redirect due to expired OTP
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup'))  # Replace 'signup' with the actual name of your signup URL

    def test_otp_verification_incorrect(self):
        # Test OTP verification with incorrect OTP
        response = self.client.post(reverse('otp_verification'), {'otp': 'wrong_otp'})
        self.assertFalse(User.objects.filter(username=self.credentials['username']).exists())
        self.assertContains(response, 'Invalid OTP')
