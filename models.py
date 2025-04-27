from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables for many-to-many relationships
content_skills = db.Table('content_skills',
    db.Column('content_id', db.Integer, db.ForeignKey('content.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

event_skills = db.Table('event_skills',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

roadmap_skills = db.Table('roadmap_skills',
    db.Column('roadmap_id', db.Integer, db.ForeignKey('roadmap.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class User(UserMixin, db.Model):
    """User model for authentication and profile information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # One-to-one relationship with UserProfile
    profile = db.relationship('UserProfile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    
    # One-to-many relationships
    content_bookmarks = db.relationship('ContentBookmark', back_populates='user', cascade='all, delete-orphan')
    event_bookmarks = db.relationship('EventBookmark', back_populates='user', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', back_populates='user', cascade='all, delete-orphan')
    roadmap_progresses = db.relationship('RoadmapProgress', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserProfile(db.Model):
    """Extended user profile information."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    education_level = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))  # URL to profile image
    
    # Relationships
    user = db.relationship('User', back_populates='profile')
    skills = db.relationship('Skill', secondary='user_skills')
    
    def __repr__(self):
        return f'<UserProfile for {self.user.username}>'

# Association table for user skills
user_skills = db.Table('user_skills',
    db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profile.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class Skill(db.Model):
    """Skills that can be associated with users, content, events, and roadmaps."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100))  # e.g., Programming, Design, Data Science
    
    def __repr__(self):
        return f'<Skill {self.name}>'

class Content(db.Model):
    """Learning resources in the Collect module."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50), nullable=False)  # article, video, course, tutorial
    difficulty_level = db.Column(db.String(50))  # beginner, intermediate, advanced
    source_name = db.Column(db.String(100))
    source_url = db.Column(db.String(255))
    author = db.Column(db.String(100))
    estimated_time = db.Column(db.Integer)  # in minutes
    is_free = db.Column(db.Boolean, default=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', secondary=content_skills, backref=db.backref('contents', lazy='dynamic'))
    bookmarks = db.relationship('ContentBookmark', back_populates='content', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', back_populates='content', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Content {self.title}>'

class ContentBookmark(db.Model):
    """Bookmarks for learning resources."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    date_bookmarked = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', back_populates='content_bookmarks')
    content = db.relationship('Content', back_populates='bookmarks')
    
    # Ensure a user can bookmark a content only once
    __table_args__ = (db.UniqueConstraint('user_id', 'content_id'),)
    
    def __repr__(self):
        return f'<ContentBookmark {self.user.username} - {self.content.title}>'

class Event(db.Model):
    """Tech events in the Connect module."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))  # physical location or "Online"
    is_online = db.Column(db.Boolean, default=False)
    event_date = db.Column(db.DateTime, nullable=False)
    registration_url = db.Column(db.String(255))
    organizer = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', secondary=event_skills, backref=db.backref('events', lazy='dynamic'))
    bookmarks = db.relationship('EventBookmark', back_populates='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'

class EventBookmark(db.Model):
    """Bookmarks for tech events."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    date_bookmarked = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    set_reminder = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', back_populates='event_bookmarks')
    event = db.relationship('Event', back_populates='bookmarks')
    
    # Ensure a user can bookmark an event only once
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id'),)
    
    def __repr__(self):
        return f'<EventBookmark {self.user.username} - {self.event.title}>'

class Quiz(db.Model):
    """Quizzes for skill assessment."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    difficulty_level = db.Column(db.String(50))
    time_limit = db.Column(db.Integer)  # in minutes
    passing_score = db.Column(db.Integer, default=70)  # percentage
    
    # Relationships
    content = db.relationship('Content', back_populates='quizzes')
    questions = db.relationship('QuizQuestion', back_populates='quiz', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', back_populates='quiz', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class QuizQuestion(db.Model):
    """Questions for quizzes."""
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='multiple_choice')  # multiple_choice, true_false, short_answer
    points = db.Column(db.Integer, default=1)
    
    # Relationships
    quiz = db.relationship('Quiz', back_populates='questions')
    options = db.relationship('QuizOption', back_populates='question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizQuestion {self.id} for Quiz {self.quiz_id}>'

class QuizOption(db.Model):
    """Options for quiz questions."""
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    
    # Relationships
    question = db.relationship('QuizQuestion', back_populates='options')
    
    def __repr__(self):
        return f'<QuizOption {self.id} for Question {self.question_id}>'

class QuizAttempt(db.Model):
    """User attempts at quizzes."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float)  # Percentage score
    passed = db.Column(db.Boolean)
    
    # Relationships
    user = db.relationship('User', back_populates='quiz_attempts')
    quiz = db.relationship('Quiz', back_populates='attempts')
    answers = db.relationship('QuizAnswer', back_populates='attempt', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizAttempt {self.id} by {self.user.username}>'

class QuizAnswer(db.Model):
    """User answers for quiz questions."""
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('quiz_option.id'))
    text_answer = db.Column(db.Text)  # For short answer questions
    is_correct = db.Column(db.Boolean)
    
    # Relationships
    attempt = db.relationship('QuizAttempt', back_populates='answers')
    question = db.relationship('QuizQuestion')
    selected_option = db.relationship('QuizOption')
    
    def __repr__(self):
        return f'<QuizAnswer {self.id} for Attempt {self.attempt_id}>'

class Roadmap(db.Model):
    """Learning roadmaps in the Crux module."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(50))
    estimated_completion_time = db.Column(db.Integer)  # in days
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', secondary=roadmap_skills, backref=db.backref('roadmaps', lazy='dynamic'))
    topics = db.relationship('RoadmapTopic', back_populates='roadmap', cascade='all, delete-orphan')
    progresses = db.relationship('RoadmapProgress', back_populates='roadmap', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Roadmap {self.title}>'

class RoadmapTopic(db.Model):
    """Topics within roadmaps."""
    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmap.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)  # Order within the roadmap
    parent_id = db.Column(db.Integer, db.ForeignKey('roadmap_topic.id'))  # For hierarchical topics
    
    # Relationships
    roadmap = db.relationship('Roadmap', back_populates='topics')
    parent = db.relationship('RoadmapTopic', remote_side=[id], backref=db.backref('subtopics', lazy='dynamic'))
    resources = db.relationship('RoadmapResource', back_populates='topic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RoadmapTopic {self.title} for Roadmap {self.roadmap_id}>'

class RoadmapResource(db.Model):
    """Resources associated with roadmap topics."""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('roadmap_topic.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    title = db.Column(db.String(255))  # For external resources
    description = db.Column(db.Text)
    url = db.Column(db.String(255))  # For external resources
    order = db.Column(db.Integer, nullable=False)  # Order within the topic
    
    # Relationships
    topic = db.relationship('RoadmapTopic', back_populates='resources')
    content = db.relationship('Content')
    
    def __repr__(self):
        return f'<RoadmapResource {self.id} for Topic {self.topic_id}>'

class RoadmapProgress(db.Model):
    """User progress through roadmaps."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmap.id'), nullable=False)
    started_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Relationships
    user = db.relationship('User', back_populates='roadmap_progresses')
    roadmap = db.relationship('Roadmap', back_populates='progresses')
    topic_progresses = db.relationship('TopicProgress', back_populates='roadmap_progress', cascade='all, delete-orphan')
    
    # Ensure a user can have only one progress record per roadmap
    __table_args__ = (db.UniqueConstraint('user_id', 'roadmap_id'),)
    
    def __repr__(self):
        return f'<RoadmapProgress {self.id} for User {self.user_id} on Roadmap {self.roadmap_id}>'

class TopicProgress(db.Model):
    """User progress on individual roadmap topics."""
    id = db.Column(db.Integer, primary_key=True)
    roadmap_progress_id = db.Column(db.Integer, db.ForeignKey('roadmap_progress.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('roadmap_topic.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime)
    
    # Relationships
    roadmap_progress = db.relationship('RoadmapProgress', back_populates='topic_progresses')
    topic = db.relationship('RoadmapTopic')
    
    # Ensure a progress record can have only one entry per topic
    __table_args__ = (db.UniqueConstraint('roadmap_progress_id', 'topic_id'),)
    
    def __repr__(self):
        return f'<TopicProgress {self.id} for Topic {self.topic_id}>'
