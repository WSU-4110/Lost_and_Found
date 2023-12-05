from unittest import TestCase, mock
from main.forms import ReportForm
from main.models import Report

class ReportFormTest(TestCase):
    def setUp(self):
        self.form = ReportForm()
        self.mock_report = mock.create_autospec(Report, instance=True)

    @mock.patch.object(ReportForm, 'save')
    def test_save(self, mock_save):
        mock_save.return_value = self.mock_report
        self.form.save()
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
