from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import Report

class ReportExistenceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='yvaskiv', password='s0Rry/40lera')
        self.report = Report.objects.create(
            Name='Test Report',
            Brand='Test Brand',
            Location='Test Location',
            Category='Test Category',
            description='Test Description',
            author=self.user,
            date_created=timezone.now().date()
        )

    def test_report_exists(self):
        date_created = self.report.date_created
        report_exists = Report.objects.filter(date_created=date_created).exists()
        self.assertTrue(report_exists)