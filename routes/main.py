from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Content, Event, Roadmap, Skill
from app import db
from utils import difficulty_color, content_type_icon

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main landing page."""
    # Get featured items for each module
    featured_content = Content.query.order_by(Content.date_added.desc()).limit(3).all()
    upcoming_events = Event.query.filter(Event.event_date >= db.func.current_date()).order_by(Event.event_date).limit(3).all()
    featured_roadmaps = Roadmap.query.order_by(Roadmap.created_date.desc()).limit(3).all()
    
    # Get popular skills
    popular_skills = Skill.query.limit(10).all()
    
    return render_template('index.html', 
                          featured_content=featured_content,
                          upcoming_events=upcoming_events,
                          featured_roadmaps=featured_roadmaps,
                          popular_skills=popular_skills,
                          difficulty_color=difficulty_color,
                          content_type_icon=content_type_icon)

@main_bp.route('/search')
def search():
    """Global search functionality."""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    # Search in content
    content_results = Content.query.filter(
        Content.title.ilike(f'%{query}%') | Content.description.ilike(f'%{query}%')
    ).all()
    
    # Search in events
    event_results = Event.query.filter(
        Event.title.ilike(f'%{query}%') | Event.description.ilike(f'%{query}%')
    ).all()
    
    # Search in roadmaps
    roadmap_results = Roadmap.query.filter(
        Roadmap.title.ilike(f'%{query}%') | Roadmap.description.ilike(f'%{query}%')
    ).all()
    
    return render_template('search_results.html', 
                          query=query,
                          content_results=content_results,
                          event_results=event_results,
                          roadmap_results=roadmap_results,
                          difficulty_color=difficulty_color,
                          content_type_icon=content_type_icon)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with personalized content."""
    # Get user's bookmarked content
    bookmarked_content = [bookmark.content for bookmark in current_user.content_bookmarks]
    
    # Get user's bookmarked events
    bookmarked_events = [bookmark.event for bookmark in current_user.event_bookmarks]
    
    # Get user's roadmap progress
    roadmap_progress = current_user.roadmap_progresses
    
    # Get recommended content based on user's skills
    user_skills = []
    if current_user.profile and current_user.profile.skills:
        user_skills = [skill.id for skill in current_user.profile.skills]
    
    if user_skills:
        recommended_content = Content.query.join(
            Content.skills
        ).filter(
            Skill.id.in_(user_skills)
        ).filter(
            ~Content.id.in_([content.id for content in bookmarked_content])
        ).limit(5).all()
    else:
        recommended_content = Content.query.order_by(db.func.random()).limit(5).all()
    
    return render_template('dashboard.html',
                          bookmarked_content=bookmarked_content,
                          bookmarked_events=bookmarked_events,
                          roadmap_progress=roadmap_progress,
                          recommended_content=recommended_content,
                          difficulty_color=difficulty_color,
                          content_type_icon=content_type_icon)
