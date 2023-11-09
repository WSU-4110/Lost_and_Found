from django.contrib.auth.models import User
from .models import Post

author = User.objects.get(username='yvaskiv')
post = Post(title='StudentID', description='lost student ID, yesterday by parking structure 5', author=author)
post.save()


from django.contrib.auth.models import User
users = User.objects.all()
for user in users:
    print(user.username)