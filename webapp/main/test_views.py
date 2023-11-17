from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime

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
        self.assertRedirects(response, reverse('home'))
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
