from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main import views  

class TestUrls(SimpleTestCase):

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, views.signup)

    def test_otp_verification_url_resolves(self):
        url = reverse('otp_verification')
        self.assertEquals(resolve(url).func, views.otp_verification)




