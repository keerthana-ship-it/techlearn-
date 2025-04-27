from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from models import User, UserProfile, Skill
from forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm, ProfileForm
from utils import send_verification_email, send_password_reset_email, get_skills_dict, verify_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                # Always allow login regardless of verification status for development
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                next_page = request.args.get('next')
                if next_page and not next_page.startswith('/'):
                    next_page = None
                
                # Send the user to the dashboard by default
                return redirect(next_page or url_for('main.dashboard'))
                
            flash('Invalid email or password', 'danger')
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                phone=form.phone.data if form.phone.data else None,
                is_verified=True  # Auto-verify for now to avoid email issues
            )
            user.set_password(form.password.data)
            
            # Create user profile
            profile = UserProfile(user=user)
            
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()
            
            # Try to send verification email but don't block registration if it fails
            try:
                send_verification_email(user)
                flash('Registration successful! Please check your email to verify your account.', 'success')
            except Exception as e:
                current_app.logger.error(f"Failed to send verification email: {str(e)}")
                flash('Registration successful! You can now log in.', 'success')
            
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash(f'Error during registration: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify user email."""
    email = verify_token(token, salt='email-verification-salt')
    if email:
        # Find the user associated with this token
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Mark user as verified
            user.is_verified = True
            db.session.commit()
            
            flash('Your email has been verified! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
    
    flash('The verification link is invalid or has expired.', 'danger')
    return redirect(url_for('main.index'))

@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        # Always show this message even if email doesn't exist (security)
        flash('Check your email for instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, title='Reset Password')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = verify_token(token, salt='password-reset-salt')
    if not email:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    # Find the user associated with this token
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Update password
        user.set_password(form.password.data)
        db.session.commit()
        
        flash('Your password has been reset. You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, title='Reset Password')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit user profile."""
    # Get all skills for form choices
    all_skills = Skill.query.all()
    
    form = ProfileForm(
        original_username=current_user.username,
        original_email=current_user.email,
        original_phone=current_user.phone
    )
    form.skills.choices = [(skill.id, skill.name) for skill in all_skills]
    
    if form.validate_on_submit():
        # Update user information
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data if form.phone.data else None
        
        # Update profile information
        profile = current_user.profile or UserProfile(user=current_user)
        profile.location = form.location.data
        profile.bio = form.bio.data
        profile.education_level = form.education_level.data
        
        # Update skills
        selected_skills = Skill.query.filter(Skill.id.in_(form.skills.data)).all()
        profile.skills = selected_skills
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        
        if current_user.profile:
            form.location.data = current_user.profile.location
            form.bio.data = current_user.profile.bio
            form.education_level.data = current_user.profile.education_level
            
            # Set selected skills
            if current_user.profile.skills:
                form.skills.data = [skill.id for skill in current_user.profile.skills]
    
    return render_template('auth/profile.html', form=form)
