from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bcrypt import Bcrypt
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database & Login System
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# For Password Hashing
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'{self.username}'

# Database Tables
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=str(datetime.now()))
    message = db.Column(db.Text)

    def __repr__(self):
        return f'{self.name}'

class DownloadCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.count}'

# Create Tables if do not exist
with app.app_context():
    db.create_all()

# Authenticarion System
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already Logged In.", "info")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Home
@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(name)
        print(email)
        print(message)
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
        flash("Thankyou. We will get in touch with you soon.!")
        return redirect(url_for('home'))
    return render_template('index.html')

# Projects
@app.route("/bad")
def bad():
    return render_template('bad.html')

@app.route("/3dprinter")
def dprinter():
    return render_template('3dprinter.html')

@app.route("/lms")
def lms():
    return render_template('lms.html')

@app.route("/trading_bot")
def trading_bot():
    return render_template('trading_bot.html')

@app.route("/summarizer")
def summarizer():
    return render_template('summarizer.html')

@app.route("/yupbot")
def yupbot():
    return render_template('yupbot.html')

# Download resume
@app.route('/downloadResume') # this is a job for GET, not POST
def downloadResume():
    if not DownloadCount.query.first():
        default_count = DownloadCount(count=0)
        db.session.add(default_count)
        db.session.commit()
    else:
        download_counter = DownloadCount.query.first()
        download_counter.count += 1
        db.session.commit()
    return send_file(
        'resume.pdf',
        download_name='Shashishekhar Python Developer.pdf',
        as_attachment=True
    )

# Admin Section
@app.route("/admin/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user_list.html", users=users)


@app.route("/admin")
def admin():
    user_count = User.query.count()
    message_count = Contact.query.count()
    download_counter = DownloadCount.query.first()
    download_count = download_counter.count
    context = {
        'user_count': user_count,
        'message_count': message_count,
        'download_count':download_count
    }
    return render_template("admin_base.html", **context)



if __name__== "__main__":
    app.run()


# flask run --debug