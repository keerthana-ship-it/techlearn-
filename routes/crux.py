from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from models import Roadmap, RoadmapTopic, RoadmapProgress, TopicProgress, Skill
from forms import RoadmapFilterForm
from utils import get_skills_dict, calculate_completion_percentage, difficulty_color

crux_bp = Blueprint('crux', __name__)

@crux_bp.route('/')
def index():
    """Main page for learning paths (Crux module)."""
    # Get all skills for filter form
    all_skills = Skill.query.all()
    
    # Initialize filter form
    form = RoadmapFilterForm()
    form.skills.choices = [(skill.id, skill.name) for skill in all_skills]
    
    # Process filter parameters
    skill_ids = request.args.getlist('skills', type=int)
    difficulty = request.args.get('difficulty', '')
    search = request.args.get('search', '')
    
    # Build query with filters
    query = Roadmap.query
    
    # Filter by skills
    if skill_ids:
        query = query.join(Roadmap.skills).filter(Skill.id.in_(skill_ids))
    
    # Filter by difficulty
    if difficulty:
        query = query.filter(Roadmap.difficulty_level == difficulty)
    
    # Filter by search term
    if search:
        query = query.filter(
            Roadmap.title.ilike(f'%{search}%') | 
            Roadmap.description.ilike(f'%{search}%')
        )
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    per_page = 9
    roadmap_pagination = query.order_by(Roadmap.title).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Pre-select form values from request
    if skill_ids:
        form.skills.data = skill_ids
    form.difficulty.data = difficulty
    form.search.data = search
    
    # Get user's roadmap progress
    user_progress = {}
    if current_user.is_authenticated:
        for progress in current_user.roadmap_progresses:
            user_progress[progress.roadmap_id] = progress.completion_percentage
    
    return render_template('crux/index.html',
                          form=form,
                          roadmap_pagination=roadmap_pagination,
                          user_progress=user_progress,
                          difficulty_color=difficulty_color)

@crux_bp.route('/roadmap/<int:roadmap_id>')
def roadmap_detail(roadmap_id):
    """View details of a learning roadmap."""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    # Get topics organized by parent/child relationships
    topics = RoadmapTopic.query.filter_by(
        roadmap_id=roadmap_id, parent_id=None
    ).order_by(RoadmapTopic.order).all()
    
    # Get user progress for this roadmap
    user_progress = None
    topic_completions = {}
    if current_user.is_authenticated:
        progress = RoadmapProgress.query.filter_by(
            user_id=current_user.id, roadmap_id=roadmap_id
        ).first()
        
        if progress:
            user_progress = progress
            # Create dictionary of completed topics
            for topic_progress in progress.topic_progresses:
                topic_completions[topic_progress.topic_id] = topic_progress.completed
    
    return render_template('crux/roadmap_detail.html',
                          roadmap=roadmap,
                          topics=topics,
                          user_progress=user_progress,
                          topic_completions=topic_completions,
                          difficulty_color=difficulty_color)

@crux_bp.route('/start-roadmap/<int:roadmap_id>', methods=['POST'])
@login_required
def start_roadmap(roadmap_id):
    """Start a roadmap learning path."""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    # Check if already started
    existing_progress = RoadmapProgress.query.filter_by(
        user_id=current_user.id, roadmap_id=roadmap_id
    ).first()
    
    if existing_progress:
        flash('You have already started this roadmap.', 'info')
    else:
        # Create progress record
        progress = RoadmapProgress(
            user_id=current_user.id,
            roadmap_id=roadmap_id,
            completion_percentage=0.0
        )
        db.session.add(progress)
        
        # Create topic progress records for all topics
        topics = RoadmapTopic.query.filter_by(roadmap_id=roadmap_id).all()
        for topic in topics:
            topic_progress = TopicProgress(
                roadmap_progress=progress,
                topic_id=topic.id,
                completed=False
            )
            db.session.add(topic_progress)
        
        db.session.commit()
        flash('Roadmap started! Track your progress as you learn.', 'success')
    
    return redirect(url_for('crux.roadmap_detail', roadmap_id=roadmap_id))

@crux_bp.route('/mark-topic/<int:topic_id>', methods=['POST'])
@login_required
def mark_topic(topic_id):
    """Mark a topic as complete or incomplete."""
    topic = RoadmapTopic.query.get_or_404(topic_id)
    
    # Get user progress for this roadmap
    progress = RoadmapProgress.query.filter_by(
        user_id=current_user.id, roadmap_id=topic.roadmap_id
    ).first_or_404()
    
    # Get topic progress
    topic_progress = TopicProgress.query.filter_by(
        roadmap_progress_id=progress.id, topic_id=topic_id
    ).first_or_404()
    
    # Toggle completion status
    topic_progress.completed = not topic_progress.completed
    if topic_progress.completed:
        topic_progress.completed_date = db.func.current_timestamp()
    else:
        topic_progress.completed_date = None
    
    # Update overall progress percentage
    total_topics = TopicProgress.query.filter_by(roadmap_progress_id=progress.id).count()
    completed_topics = TopicProgress.query.filter_by(
        roadmap_progress_id=progress.id, completed=True
    ).count()
    
    progress.completion_percentage = calculate_completion_percentage(completed_topics, total_topics)
    progress.last_updated = db.func.current_timestamp()
    
    db.session.commit()
    
    status = 'completed' if topic_progress.completed else 'marked as incomplete'
    flash(f'Topic "{topic.title}" {status}.', 'success')
    
    return redirect(url_for('crux.roadmap_detail', roadmap_id=topic.roadmap_id))

@crux_bp.route('/reset-progress/<int:roadmap_id>', methods=['POST'])
@login_required
def reset_progress(roadmap_id):
    """Reset progress for a roadmap."""
    progress = RoadmapProgress.query.filter_by(
        user_id=current_user.id, roadmap_id=roadmap_id
    ).first_or_404()
    
    # Reset all topic progress
    for topic_progress in progress.topic_progresses:
        topic_progress.completed = False
        topic_progress.completed_date = None
    
    progress.completion_percentage = 0.0
    progress.last_updated = db.func.current_timestamp()
    
    db.session.commit()
    flash('Progress has been reset.', 'info')
    
    return redirect(url_for('crux.roadmap_detail', roadmap_id=roadmap_id))
