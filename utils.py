import os
import secrets
import json
import itsdangerous
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_mail import Message
from app import mail

def get_serializer():
    """Get a serializer for secure tokens with configurable expiration."""
    secret_key = current_app.config['SECRET_KEY']
    return itsdangerous.URLSafeTimedSerializer(secret_key)

def send_verification_email(user):
    """Send email verification to the user."""
    serializer = get_serializer()
    # Generate a secure token with the user's email
    token = serializer.dumps(user.email, salt='email-verification-salt')
    
    try:
        msg = Message('TechLearn - Email Verification',
                    recipients=[user.email])
        msg.body = f'''To verify your TechLearn account, please click on the following link:
{url_for('auth.verify_email', token=token, _external=True)}

This link will expire in 24 hours.

If you did not register for TechLearn, please ignore this email.
'''
        mail.send(msg)
        current_app.logger.info(f"Verification email sent to {user.email}")
        return token
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        # Automatically verify the user since email might not work in development
        user.is_verified = True
        return token

def send_password_reset_email(user):
    """Send password reset email to the user."""
    serializer = get_serializer()
    # Generate a secure token with the user's email
    token = serializer.dumps(user.email, salt='password-reset-salt')
    
    try:
        msg = Message('TechLearn - Password Reset',
                    recipients=[user.email])
        msg.body = f'''To reset your password, please click on the following link:
{url_for('auth.reset_password', token=token, _external=True)}

This link will expire in 24 hours.

If you did not request a password reset, please ignore this email.
'''
        mail.send(msg)
        current_app.logger.info(f"Password reset email sent to {user.email}")
        return token
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email: {str(e)}")
        return token

def send_event_reminder(user, event):
    """Send event reminder to the user."""
    msg = Message(f'TechLearn - Reminder: {event.title}',
                 recipients=[user.email])
    
    event_date_str = event.event_date.strftime('%A, %B %d, %Y at %I:%M %p')
    msg.body = f'''This is a reminder for the event you bookmarked:

Event: {event.title}
Date: {event_date_str}
Location: {event.location}

You can view the event details here:
{url_for('connect.event_detail', event_id=event.id, _external=True)}

Thank you for using TechLearn!
'''
    mail.send(msg)

def generate_token():
    """Generate a secure token for email verification or password reset."""
    return secrets.token_urlsafe(32)

def verify_token(token, salt='email-verification-salt', expiration=86400):
    """
    Verify the provided token.
    
    Args:
        token: The token to verify
        salt: The salt used during token generation
        expiration: Token expiration time in seconds (default 24 hours)
        
    Returns:
        The email address if the token is valid, None otherwise
    """
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
        return email
    except itsdangerous.BadSignature:
        current_app.logger.warning("Invalid token signature")
        return None
    except itsdangerous.SignatureExpired:
        current_app.logger.warning("Expired token")
        return None
    except Exception as e:
        current_app.logger.error(f"Token verification error: {str(e)}")
        return None

def format_datetime(dt):
    """Format datetime object for display."""
    if not dt:
        return ""
    return dt.strftime('%Y-%m-%d %H:%M')

def format_date(dt):
    """Format date for display."""
    if not dt:
        return ""
    return dt.strftime('%Y-%m-%d')

def get_skills_dict(skills):
    """Convert skills list to dictionary for form selection."""
    return {skill.id: skill.name for skill in skills}

def calculate_completion_percentage(completed_topics, total_topics):
    """Calculate the completion percentage for a roadmap."""
    if total_topics == 0:
        return 0
    return (completed_topics / total_topics) * 100

def difficulty_color(level):
    """Return Bootstrap color class based on difficulty level."""
    colors = {
        'beginner': 'success',
        'intermediate': 'warning',
        'advanced': 'danger'
    }
    return colors.get(level.lower(), 'secondary')

def content_type_icon(type_name):
    """Return FontAwesome icon class based on content type."""
    icons = {
        'article': 'fa-file-alt',
        'video': 'fa-video',
        'course': 'fa-graduation-cap',
        'tutorial': 'fa-book-open'
    }
    return icons.get(type_name.lower(), 'fa-file')
