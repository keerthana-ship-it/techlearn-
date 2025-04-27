from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from app import db
from models import Event, EventBookmark, Skill
from forms import EventFilterForm, EventBookmarkForm
from utils import get_skills_dict, send_event_reminder
from config import Config

connect_bp = Blueprint('connect', __name__)

@connect_bp.route('/')
def index():
    """Main page for tech events (Connect module)."""
    # Get all skills for filter form
    all_skills = Skill.query.all()
    
    # Initialize filter form
    form = EventFilterForm()
    form.skills.choices = [(skill.id, skill.name) for skill in all_skills]
    
    # Process filter parameters
    location = request.args.get('location', Config.DEFAULT_LOCATION)
    event_type = request.args.get('event_type', '')
    skill_ids = request.args.getlist('skills', type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    search = request.args.get('search', '')
    
    # Build query with filters
    query = Event.query
    
    # Filter by location if not empty
    if location:
        query = query.filter(Event.location.ilike(f'%{location}%'))
    
    # Filter by event type
    if event_type == 'online':
        query = query.filter(Event.is_online == True)
    elif event_type == 'offline':
        query = query.filter(Event.is_online == False)
    
    # Filter by skills
    if skill_ids:
        query = query.join(Event.skills).filter(Skill.id.in_(skill_ids))
    
    # Filter by date range
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Event.event_date >= start_date_obj)
        except ValueError:
            pass
    else:
        # Default to showing future events
        query = query.filter(Event.event_date >= datetime.now())
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            # Make end_date inclusive by setting it to end of day
            end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)
            query = query.filter(Event.event_date <= end_date_obj)
        except ValueError:
            pass
    
    # Filter by search term
    if search:
        query = query.filter(
            Event.title.ilike(f'%{search}%') | 
            Event.description.ilike(f'%{search}%') |
            Event.organizer.ilike(f'%{search}%')
        )
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    per_page = 10
    event_pagination = query.order_by(Event.event_date).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Pre-select form values from request
    form.location.data = location
    form.event_type.data = event_type
    if skill_ids:
        form.skills.data = skill_ids
    if start_date:
        try:
            form.start_date.data = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            pass
    if end_date:
        try:
            form.end_date.data = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            pass
    form.search.data = search
    
    # Get bookmarked event IDs for current user
    bookmarked_ids = []
    if current_user.is_authenticated:
        bookmarked_ids = [bookmark.event_id for bookmark in current_user.event_bookmarks]
    
    return render_template('connect/index.html',
                          form=form,
                          event_pagination=event_pagination,
                          bookmarked_ids=bookmarked_ids,
                          default_location=Config.DEFAULT_LOCATION)

@connect_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """View details of an event."""
    event = Event.query.get_or_404(event_id)
    
    # Check if event is bookmarked by current user
    is_bookmarked = False
    bookmark = None
    if current_user.is_authenticated:
        bookmark = EventBookmark.query.filter_by(
            user_id=current_user.id, event_id=event_id
        ).first()
        is_bookmarked = bookmark is not None
    
    # Get related events based on skills
    skill_ids = [skill.id for skill in event.skills]
    related_events = []
    if skill_ids:
        related_events = Event.query.join(
            Event.skills
        ).filter(
            Skill.id.in_(skill_ids)
        ).filter(
            Event.id != event_id,
            Event.event_date >= datetime.now()
        ).order_by(Event.event_date).limit(3).all()
    
    bookmark_form = EventBookmarkForm()
    if bookmark:
        bookmark_form.notes.data = bookmark.notes
        bookmark_form.set_reminder.data = bookmark.set_reminder
    
    return render_template('connect/event_detail.html',
                          event=event,
                          is_bookmarked=is_bookmarked,
                          bookmark=bookmark,
                          bookmark_form=bookmark_form,
                          related_events=related_events)

@connect_bp.route('/bookmark/<int:event_id>', methods=['POST'])
@login_required
def bookmark_event(event_id):
    """Bookmark or update bookmark for event."""
    event = Event.query.get_or_404(event_id)
    
    # Check if already bookmarked
    bookmark = EventBookmark.query.filter_by(
        user_id=current_user.id, event_id=event_id
    ).first()
    
    form = EventBookmarkForm()
    if form.validate_on_submit():
        if bookmark:
            # Update existing bookmark
            bookmark.notes = form.notes.data
            bookmark.set_reminder = form.set_reminder.data
            flash('Bookmark updated', 'success')
        else:
            # Create new bookmark
            bookmark = EventBookmark(
                user_id=current_user.id,
                event_id=event_id,
                notes=form.notes.data,
                set_reminder=form.set_reminder.data
            )
            db.session.add(bookmark)
            flash('Event bookmarked', 'success')
        
        db.session.commit()
        
        # Send reminder email if requested and event is in the future
        if bookmark.set_reminder and event.event_date > datetime.now():
            send_event_reminder(current_user, event)
            flash('Reminder email sent', 'info')
    
    return redirect(url_for('connect.event_detail', event_id=event_id))

@connect_bp.route('/remove-bookmark/<int:event_id>', methods=['POST'])
@login_required
def remove_bookmark(event_id):
    """Remove bookmark from event."""
    bookmark = EventBookmark.query.filter_by(
        user_id=current_user.id, event_id=event_id
    ).first_or_404()
    
    db.session.delete(bookmark)
    db.session.commit()
    
    flash('Bookmark removed', 'info')
    return redirect(url_for('connect.event_detail', event_id=event_id))

@connect_bp.route('/calendar')
def calendar():
    """View events in calendar format."""
    # Get date range from request or default to current month
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # Calculate start and end dates for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get events for the month
    events = Event.query.filter(
        Event.event_date >= start_date,
        Event.event_date <= end_date.replace(hour=23, minute=59, second=59)
    ).order_by(Event.event_date).all()
    
    # Organize events by day
    calendar_days = {}
    for day in range(1, end_date.day + 1):
        calendar_days[day] = []
    
    for event in events:
        day = event.event_date.day
        calendar_days[day].append(event)
    
    return render_template('connect/calendar.html',
                          year=year,
                          month=month,
                          calendar_days=calendar_days,
                          month_name=start_date.strftime('%B'))
