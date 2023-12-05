from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import Report
from main.forms import ReportForm
from unittest import mock

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

    def test_save_form(self):
        form = ReportForm(data={
            'Name': 'Test Report',
            'Brand': 'Test Brand',
            'Location': 'Test Location',
            'Category': 'Test Category',
            'description': 'Test Description',
        })
        with mock.patch.object(ReportForm, 'save') as mock_save:
            mock_report = mock.create_autospec(Report, instance=True)
            mock_save.return_value = mock_report
            form.save()
            self.assertTrue(mock_save.called)

    def test_form_valid(self):
        form = ReportForm(data={
            'Name': 'Test Report',
            'Brand': 'Test Brand',
            'Location': 'Test Location',
            'Category': 'Test Category',
            'description': 'Test Description',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = ReportForm(data={
            'Name': 'Test Report',
            'Brand': 'Test Brand',
            'Location': 'Test Location',
            'Category': 'Test Category',
            'description': '',
        })
        self.assertFalse(form.is_valid())   

    def test_form_invalid2(self):
        form = ReportForm(data={
            'Name': 'Test Report',
            'Brand': 'Test Brand1',
            'Location': 'Test Location',
            'Category': '',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())

    def test_form_invalid3(self):        
        form = ReportForm(data={
            'Name': 'Test Report',
            'Brand': '',
            'Location': 'Test Location',
            'Category': 'Test Category',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())

    def test_form_invalid4(self):
        form = ReportForm(data={
            'Name': '',
            'Brand': 'Test Brand',
            'Location': 'Test Location',
            'Category': 'Test Category',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())
