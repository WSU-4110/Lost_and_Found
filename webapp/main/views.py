from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from datetime import datetime
from .forms import RegisterForm
import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
#from .models import ChatRoom, Message
#from .forms import MessageForm
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Report
from .forms import ReportForm
from .forms import DiscussionForm
from .models import Discussion
import cv2
import numpy as np
from django.utils import timezone
import pytz


# Get the current time in UTC
now_utc = timezone.now()

# Convert to Eastern Time
eastern_tz = pytz.timezone('America/New_York')
now_eastern = now_utc.astimezone(eastern_tz)

# Create your views here.
@login_required(login_url='/login')
def home(request):

    eastern = pytz.timezone('US/Eastern')
    date = request.GET.get('date')
    title = request.GET.get('title')
    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        posts = Post.objects.filter(date_created__date=date)
    elif title:
        posts = Post.objects.filter(title__icontains=title)
    else:
        posts = Post.objects.all()
        posts = Post.objects.all().order_by('-date_created')
    return render(request, 'main/home.html', {'posts': posts})


def list_report(request):
    #reports = Report.objects.filter(is_resolved=False)
    #print(reports)
    name = request.GET.get('name')
    date_str = request.GET.get('date')
    brand = request.GET.get('brand')
    place = request.GET.get('location')
    category = request.GET.get('category')
    author = request.GET.get('author')
    if name:
        reports = Report.objects.filter(Name__icontains=name, is_resolved=False)
    elif date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        reports = Report.objects.filter(date_created=date, is_resolved=False)
    elif brand:
        reports = Report.objects.filter(Brand__icontains=brand, is_resolved=False)
    elif place:
        reports = Report.objects.filter(Location__icontains=place, is_resolved=False)
    elif category:
        reports = Report.objects.filter(Category__icontains=category, is_resolved=False)    
    elif author:
        reports = Report.objects.filter(author__username__icontains=author, is_resolved=False)  
    else:
        reports = Report.objects.filter(is_resolved=False).order_by('-date_created')
    discussion = Discussion.objects.filter(report__in=reports)
    return render(request, 'main/list_report.html', {'reports': reports})


def add_comment(request, report_id):
    report = Report.objects.get(id=report_id)
    discussion = Discussion.objects.filter(report=report).order_by('-date_created')
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.report = report
            discussion.author = request.user
            discussion.save()
            return redirect('list_report')
    else:
        form = DiscussionForm()
    return render(request, 'main/add_comment.html', {'form': form})

def list_discussions(request):
    discussions = Discussion.objects.all().order_by('-date_created')
    return render(request, 'main/list_discussions.html', {'discussions': discussions})


def personal_list(request):
    reports = Report.objects.filter(author=request.user)
    return render(request, 'main/personal_list.html', {'reports': reports})


def list_resolved(request):
    reports = Report.objects.filter(is_resolved=True)
    #print(reports)
    return render(request, 'main/list_resolved.html', {'reports': reports})

@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            #author_username = request.POST.get('author')
            author = User.objects.get(username=request.user.username)
            post = Post.objects.create(title=title, description=description, author=author)
            post.save()
            return redirect('home')
            
    return render(request, 'main/create_post.html', {'form': form})


def search_posts(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            posts = Post.objects.filter(date_created__range=[start_date, end_date])

        else:
            posts = Post.objects.all()

        return render(request, 'main/home.html', {'posts': posts})  
    
    return render(request, 'main/home.html', {'posts': []})  
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet
            otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
            request.session['otp'] = otp  # Store the OTP in the session
            request.session['username'] = form.cleaned_data.get('username')
            request.session['email'] = form.cleaned_data.get('email')
            request.session['password'] = form.cleaned_data.get('password1')
            request.session['otp_time'] = str(datetime.now())  # Store the current time
            send_mail(
                'Your OTP',
                f'Your OTP is {otp}',
                'lostfoundwayne@gmail.com',
                [form.cleaned_data.get('email')],
                fail_silently=False,
            )
            return redirect('otp_verification')  # Redirect to OTP verification view
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})



def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_time_str = request.session.get('otp_time')
        if otp_time_str:
            otp_time = datetime.strptime(otp_time_str, '%Y-%m-%d %H:%M:%S.%f')
            if datetime.now() - otp_time > timedelta(minutes=2):  # Check if more than 2 minutes have passed
                messages.error(request, 'OTP expired. Please sign up again.')
                # Redirect to the signup page
                return redirect('signup')
            elif otp == str(request.session.get('otp')):
                try:
                    User.objects.create_user(
                        username=request.session.get('username'),
                        email=request.session.get('email'),
                        password=request.session.get('password')
                    )
                    messages.success(request, 'User created successfully')
                    # Clear the session variables related to OTP
                    del request.session['otp']
                    del request.session['otp_time']
                    return redirect('home')
                except Exception as e:
                    # Handle exceptions like duplicate username
                    messages.error(request, f'Error creating user: {e}')
            else:
                messages.error(request, 'Invalid OTP')
        else:
            messages.error(request, 'OTP verification failed. Please sign up again.')
            return redirect('signup')

    return render(request, 'registration/otp_verification.html')


@login_required
def display_user(request):
    user = User.objects.get(username=request.user.username)  # Replace 'username' with the actual username
    return render(request, 'main/userprofile.html', {'user': user}) 




'''
@login_required
def create_chat_room(request):
    if request.method == 'POST':
        chat_room_name = request.POST.get('chat_room_name')
        chat_room = ChatRoom.objects.create(name=chat_room_name)
    chat_room.users.add(request.user)
    chat_room.save()
    return render(request, 'chat/chat_room.html', {'chat_room': chat_room})

@login_required
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.chat_room = chat_room
            message.save()
    return render(request, 'chat/chat_room.html', {'chat_room': chat_room})


@login_required
def fetch_messages(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')
    return render(request, 'chat/messages.html', {'messages': messages})
'''



@login_required
def create_report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('Name')
            brand = form.cleaned_data.get('Brand')
            location = form.cleaned_data.get('Location')
            category = form.cleaned_data.get('Category')
            description = form.cleaned_data.get('description')
            image_link = form.cleaned_data.get('image_link')
            author = User.objects.get(username=request.user.username)
            report = Report.objects.create(Name=name, Brand=brand, Location=location, Category=category, description=description, author=author, image_link=image_link)
            report.save()
            return redirect('home')
    return render(request, 'main/create_report.html', {'form': form})




def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user == report.author:
        report.is_resolved = True
        report.delete()
    return redirect('list_report')


def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user == report.author:
        report.is_resolved = True
        report.save()
    return redirect('list_report')



def preprocess_image(image_path):
    image = Image.open(image_path)
    grayscale_image = ImageOps.grayscale(image)
    return grayscale_image
def resize_image(image, base_width=800):
    w_percent = (base_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    resized_image = image.resize((base_width, h_size), Image.LANCZOS)
    return resized_image
def apply_threshold(image, threshold=200):
    return image.point(lambda p: p > threshold and 255)


def denoise_image(image):
    open_cv_image = np.array(image)
    # Check if the image is single-channel (grayscale)
    if len(open_cv_image.shape) == 2 or open_cv_image.shape[2] == 1:
        denoised_image = cv2.fastNlMeansDenoising(open_cv_image, None, 10, 7, 21)
    else:
        denoised_image = cv2.fastNlMeansDenoisingColored(open_cv_image, None, 10, 10, 7, 21)
    return Image.fromarray(denoised_image)
def preprocess_for_ocr(image_path):
    image = Image.open(image_path)
    image = ImageOps.grayscale(image)
    image = resize_image(image)
    image = apply_threshold(image)
    image = denoise_image(image)
    return image


def detect_id_card(image_path):
    preprocessed_image = preprocess_for_ocr(image_path)
    text = pytesseract.image_to_string(preprocessed_image,lang='eng',config='--psm 6')
    print("Extracted Text:", text)
    
    # Define patterns or keywords commonly found on ID cards
    id_patterns = [
        re.compile(r'\bName\b', re.IGNORECASE),
        re.compile(r'\bDate of Birth\b', re.IGNORECASE),
        re.compile(r'\bID Number\b', re.IGNORECASE),
        # Add more patterns as needed
    ]
    
    # Check if the text contains any of the patterns
    for pattern in id_patterns:
        if pattern.search(text):
            return "Potential ID Card Detected"
    
    return "No ID Card Detected"

def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            result = detect_id_card(image_upload.image.path)
            return render(request, 'main/image_upload.html', {'form': form, 'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'main/image_upload.html', {'form': form})





def report_form(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            return redirect('reports')  # replace 'reports' with the name of the view where you list the reports
    else:
        form = ReportForm()

    return render(request, 'main/create_report.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import Discussion

def discussion_page(request, report_id):
    # Get the report object based on the report_id
    report = get_object_or_404(Report, id=report_id)

    # Get the discussions for the report with the given id
    discussions = Discussion.objects.filter(report=report)
     
     
    # Render a template with these discussions and the report
    return render(request, 'main/discussion_page.html', {'report': report, 'discussions': discussions})
