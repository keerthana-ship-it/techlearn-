from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms import DateField, DateTimeField, IntegerField, SelectMultipleField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL, ValidationError
from models import User

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone (optional)', validators=[Optional(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        """Validate that the username is not already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Validate that the email is not already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one or reset your password.')
    
    def validate_phone(self, phone):
        """Validate that the phone number is not already registered."""
        if phone.data:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone number already registered.')

class PasswordResetRequestForm(FlaskForm):
    """Form to request password reset."""
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordResetForm(FlaskForm):
    """Form to reset password."""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

class ProfileForm(FlaskForm):
    """Form for updating user profile."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(min=10, max=20)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    education_level = SelectField('Education Level', choices=[
        ('', 'Select Education Level'),
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('doctorate', 'Doctorate'),
        ('self_taught', 'Self-taught')
    ], validators=[Optional()])
    skills = SelectMultipleField('Skills', coerce=int, validators=[Optional()])
    
    def __init__(self, original_username=None, original_email=None, original_phone=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.original_phone = original_phone
    
    def validate_username(self, username):
        """Validate that the new username is not taken by another user."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Validate that the new email is not registered to another user."""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered to another account.')
    
    def validate_phone(self, phone):
        """Validate that the new phone is not registered to another user."""
        if phone.data and phone.data != self.original_phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone number already registered to another account.')

class ContentFilterForm(FlaskForm):
    """Form for filtering learning content."""
    skills = SelectMultipleField('Skills', coerce=int, validators=[Optional()])
    difficulty = SelectField('Difficulty Level', choices=[
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], validators=[Optional()])
    content_type = SelectField('Content Type', choices=[
        ('', 'All Types'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('course', 'Course'),
        ('tutorial', 'Tutorial')
    ], validators=[Optional()])
    is_free = SelectField('Price', choices=[
        ('', 'All'),
        ('free', 'Free Only'),
        ('paid', 'Paid Only')
    ], validators=[Optional()])
    start_date = DateField('From Date', validators=[Optional()])
    end_date = DateField('To Date', validators=[Optional()])
    search = StringField('Search', validators=[Optional()])

class EventFilterForm(FlaskForm):
    """Form for filtering events."""
    location = StringField('Location', validators=[Optional()])
    event_type = SelectField('Event Type', choices=[
        ('', 'All Types'),
        ('online', 'Online Only'),
        ('offline', 'In-person Only')
    ], validators=[Optional()])
    skills = SelectMultipleField('Skills', coerce=int, validators=[Optional()])
    start_date = DateField('From Date', validators=[Optional()])
    end_date = DateField('To Date', validators=[Optional()])
    search = StringField('Search', validators=[Optional()])

class QuizAnswerForm(FlaskForm):
    """Form for submitting quiz answers."""
    # This will be dynamically populated based on the quiz questions
    pass

class ContentBookmarkForm(FlaskForm):
    """Form for bookmarking content."""
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])

class EventBookmarkForm(FlaskForm):
    """Form for bookmarking events."""
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    set_reminder = BooleanField('Set Reminder', default=False)

class RoadmapFilterForm(FlaskForm):
    """Form for filtering roadmaps."""
    skills = SelectMultipleField('Skills', coerce=int, validators=[Optional()])
    difficulty = SelectField('Difficulty Level', choices=[
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], validators=[Optional()])
    search = StringField('Search', validators=[Optional()])
