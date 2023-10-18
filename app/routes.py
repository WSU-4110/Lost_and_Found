from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.models import User
from app.forms import LoginForm, SignupForm

@app.route('/home')
def home():
    # Add logic for the home page if needed
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()

    if request.method == 'POST':
        if 'login' in request.form:
            if login_form.validate_on_submit():
                user = User.query.filter_by(username=login_form.username.data).first()
                if user is None or not user.check_password(login_form.password.data):
                    flash('Invalid username or password', 'error')
                else:
                    session['user_id'] = user.id
                    flash('Login successful', 'success')
                    print("Before redirect")
                    return redirect(url_for('home'))
                    print("After redirect")  # Check if this line is reached

        elif 'signup' in request.form:
            if signup_form.validate_on_submit():
                user = User(username=signup_form.username.data, email=signup_form.email.data)
                user.set_password(signup_form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Signup successful. You can now log in.', 'success')

    return render_template('index.html', login_form=login_form, signup_form=signup_form)


