from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import Report
from main.models import Comment

class CommentExistenceTest(TestCase):
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
        self.comment = Comment.objects.create(
            report=self.report,
            text='Test Comment',
            author=self.user,
            date_created=timezone.now().date()
        )




        

'''
    def test_fields(self):
        self.assertEqual(set(self.form.fields), {'author', 'text'})


    def test_comment_exists_by_text(self):
        text = self.comment.text
        comment_exists = Comment.objects.filter(text=text).exists()
        self.assertTrue(comment_exists) 
        
        def test_comment_exists_by_author(self):
        author = self.comment.author
        comment_exists = Comment.objects.filter(author=author).exists()
        self.assertTrue(comment_exists)
        
    def test_comment_exists_by_date_created(self):
        date_created = self.comment.date_created
        comment_exists = Comment.objects.filter(date_created=date_created).exists()
        self.assertTrue(comment_exists)
        
    def test_comment_exists_by_report(self):
        report = self.comment.report
        comment_exists = Comment.objects.filter(report=report).exists()
        self.assertTrue(comment_exists)
        '''

    
    
 