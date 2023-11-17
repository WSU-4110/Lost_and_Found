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

    def test_report_exists_by_category(self):
        category = self.report.Category
        report_exists = Report.objects.filter(Category=category).exists()
        self.assertTrue(report_exists)


    def test_report_exists_by_date(self):
        date_created = self.report.date_created
        report_exists = Report.objects.filter(date_created=date_created).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_name(self):
        name = self.report.Name
        report_exists = Report.objects.filter(Name=name).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_brand(self):
        brand = self.report.Brand
        report_exists = Report.objects.filter(Brand=brand).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_location(self):
        location = self.report.Location
        report_exists = Report.objects.filter(Location=location).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_category(self):
        category = self.report.Category
        report_exists = Report.objects.filter(Category=category).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_description(self):
        description = self.report.description
        report_exists = Report.objects.filter(description=description).exists()
        self.assertTrue(report_exists)
    
    def test_report_exists_by_author(self):
        author = self.report.author
        report_exists = Report.objects.filter(author=author).exists()
        self.assertTrue(report_exists)

    def test_report_exists_by_date_created(self):
        date_created = self.report.date_created
        report_exists = Report.objects.filter(date_created=date_created).exists()
        self.assertTrue(report_exists)

    def test_report_does_not_exist_by_name(self):
        name = 'Non-existent Report'
        report_exists = Report.objects.filter(Name=name).exists()
        self.assertFalse(report_exists)

