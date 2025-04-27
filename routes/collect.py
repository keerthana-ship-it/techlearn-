from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from models import Content, ContentBookmark, Quiz, QuizAttempt, QuizAnswer, Skill
from forms import ContentFilterForm, ContentBookmarkForm, QuizAnswerForm
from utils import get_skills_dict, difficulty_color, content_type_icon

collect_bp = Blueprint('collect', __name__)

@collect_bp.route('/')
def index():
    """Main page for learning resources (Collect module)."""
    # Get all skills for filter form
    all_skills = Skill.query.all()
    
    # Initialize filter form
    form = ContentFilterForm()
    form.skills.choices = [(skill.id, skill.name) for skill in all_skills]
    
    # Process filter parameters
    skill_ids = request.args.getlist('skills', type=int)
    difficulty = request.args.get('difficulty', '')
    content_type = request.args.get('content_type', '')
    is_free = request.args.get('is_free', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    search = request.args.get('search', '')
    
    # Build query with filters
    query = Content.query
    
    # Filter by skills
    if skill_ids:
        query = query.join(Content.skills).filter(Skill.id.in_(skill_ids))
    
    # Filter by difficulty
    if difficulty:
        query = query.filter(Content.difficulty_level == difficulty)
    
    # Filter by content type
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    # Filter by price
    if is_free == 'free':
        query = query.filter(Content.is_free == True)
    elif is_free == 'paid':
        query = query.filter(Content.is_free == False)
    
    # Filter by date range
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Content.date_added >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Content.date_added <= end_date_obj)
        except ValueError:
            pass
    
    # Filter by search term
    if search:
        query = query.filter(
            Content.title.ilike(f'%{search}%') | 
            Content.description.ilike(f'%{search}%')
        )
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    per_page = 12
    content_pagination = query.order_by(Content.date_added.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Pre-select form values from request
    if skill_ids:
        form.skills.data = skill_ids
    form.difficulty.data = difficulty
    form.content_type.data = content_type
    form.is_free.data = is_free
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
    
    # Get bookmarked content IDs for current user
    bookmarked_ids = []
    if current_user.is_authenticated:
        bookmarked_ids = [bookmark.content_id for bookmark in current_user.content_bookmarks]
    
    return render_template('collect/index.html',
                          form=form,
                          content_pagination=content_pagination,
                          bookmarked_ids=bookmarked_ids,
                          difficulty_color=difficulty_color,
                          content_type_icon=content_type_icon)

@collect_bp.route('/content/<int:content_id>')
def content_detail(content_id):
    """View details of a learning resource."""
    content = Content.query.get_or_404(content_id)
    
    # Check if content is bookmarked by current user
    is_bookmarked = False
    bookmark = None
    if current_user.is_authenticated:
        bookmark = ContentBookmark.query.filter_by(
            user_id=current_user.id, content_id=content_id
        ).first()
        is_bookmarked = bookmark is not None
    
    # Get quizzes for this content
    quizzes = Quiz.query.filter_by(content_id=content_id).all()
    
    # Get related content based on skills
    skill_ids = [skill.id for skill in content.skills]
    related_content = []
    if skill_ids:
        related_content = Content.query.join(
            Content.skills
        ).filter(
            Skill.id.in_(skill_ids)
        ).filter(
            Content.id != content_id
        ).limit(4).all()
    
    bookmark_form = ContentBookmarkForm()
    if bookmark:
        bookmark_form.notes.data = bookmark.notes
    
    return render_template('collect/content_detail.html',
                          content=content,
                          is_bookmarked=is_bookmarked,
                          bookmark=bookmark,
                          bookmark_form=bookmark_form,
                          quizzes=quizzes,
                          related_content=related_content,
                          difficulty_color=difficulty_color,
                          content_type_icon=content_type_icon)

@collect_bp.route('/bookmark/<int:content_id>', methods=['POST'])
@login_required
def bookmark_content(content_id):
    """Bookmark or update bookmark for content."""
    content = Content.query.get_or_404(content_id)
    
    # Check if already bookmarked
    bookmark = ContentBookmark.query.filter_by(
        user_id=current_user.id, content_id=content_id
    ).first()
    
    form = ContentBookmarkForm()
    if form.validate_on_submit():
        if bookmark:
            # Update existing bookmark
            bookmark.notes = form.notes.data
            flash('Bookmark updated', 'success')
        else:
            # Create new bookmark
            bookmark = ContentBookmark(
                user_id=current_user.id,
                content_id=content_id,
                notes=form.notes.data
            )
            db.session.add(bookmark)
            flash('Content bookmarked', 'success')
        
        db.session.commit()
    
    return redirect(url_for('collect.content_detail', content_id=content_id))

@collect_bp.route('/remove-bookmark/<int:content_id>', methods=['POST'])
@login_required
def remove_bookmark(content_id):
    """Remove bookmark from content."""
    bookmark = ContentBookmark.query.filter_by(
        user_id=current_user.id, content_id=content_id
    ).first_or_404()
    
    db.session.delete(bookmark)
    db.session.commit()
    
    flash('Bookmark removed', 'info')
    return redirect(url_for('collect.content_detail', content_id=content_id))

@collect_bp.route('/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Take a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if user has already passed this quiz
    existing_attempt = QuizAttempt.query.filter_by(
        user_id=current_user.id, quiz_id=quiz_id, passed=True
    ).first()
    
    if existing_attempt:
        flash(f'You have already passed this quiz with a score of {existing_attempt.score}%', 'info')
        return redirect(url_for('collect.content_detail', content_id=quiz.content_id))
    
    return render_template('collect/quiz.html', quiz=quiz)

@collect_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit quiz answers and calculate score."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Create a new quiz attempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        start_time=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.flush()  # Get attempt ID without committing transaction
    
    # Process answers
    correct_answers = 0
    total_questions = len(quiz.questions)
    total_points = sum(question.points for question in quiz.questions)
    earned_points = 0
    
    for question in quiz.questions:
        # Get selected option ID from form
        selected_option_id = request.form.get(f'question_{question.id}')
        
        # Find the selected option
        selected_option = None
        is_correct = False
        if selected_option_id:
            for option in question.options:
                if str(option.id) == selected_option_id:
                    selected_option = option
                    is_correct = option.is_correct
                    if is_correct:
                        correct_answers += 1
                        earned_points += question.points
                    break
        
        # Record the answer
        answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected_option.id if selected_option else None,
            is_correct=is_correct
        )
        db.session.add(answer)
    
    # Calculate score and update attempt
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    passed = score >= quiz.passing_score
    
    attempt.end_time = datetime.utcnow()
    attempt.score = score
    attempt.passed = passed
    
    db.session.commit()
    
    if passed:
        flash(f'Congratulations! You passed the quiz with a score of {score:.1f}%', 'success')
    else:
        flash(f'Quiz completed. Your score: {score:.1f}%. Required to pass: {quiz.passing_score}%', 'info')
    
    return redirect(url_for('collect.quiz_results', attempt_id=attempt.id))

@collect_bp.route('/quiz-results/<int:attempt_id>')
@login_required
def quiz_results(attempt_id):
    """View quiz results."""
    attempt = QuizAttempt.query.filter_by(
        id=attempt_id, user_id=current_user.id
    ).first_or_404()
    
    return render_template('collect/quiz_results.html', attempt=attempt)
