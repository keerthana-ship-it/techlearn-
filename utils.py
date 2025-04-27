import os
import secrets
from datetime import datetime
from flask import current_app, url_for
from flask_mail import Message
from app import mail

def send_verification_email(user):
    """Send email verification to the user."""
    token = generate_token()
    # Store token in database or session for verification
    
    msg = Message('TechLearn - Email Verification',
                 recipients=[user.email])
    msg.body = f'''To verify your TechLearn account, please click on the following link:
{url_for('auth.verify_email', token=token, _external=True)}

If you did not register for TechLearn, please ignore this email.
'''
    mail.send(msg)
    return token

def send_password_reset_email(user):
    """Send password reset email to the user."""
    token = generate_token()
    # Store token in database or session for verification
    
    msg = Message('TechLearn - Password Reset',
                 recipients=[user.email])
    msg.body = f'''To reset your password, please click on the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not request a password reset, please ignore this email.
'''
    mail.send(msg)
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

def verify_token(token):
    """Verify the provided token."""
    # Implement token verification logic
    # This is a placeholder and should be replaced with actual verification
    return True

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
