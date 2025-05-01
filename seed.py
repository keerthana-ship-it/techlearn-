#!/usr/bin/env python
"""
TechLearn Seed Script

This script populates the database with initial data.
Run it after setting up the database tables:
    python seed.py
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask
from app import db, create_app
from models import User, Skill, Content, Event, Roadmap, RoadmapTopic, RoadmapResource
from werkzeug.security import generate_password_hash

def seed_skills():
    """Seed skills for content and user profiles."""
    skills_data = [
        {"name": "Python", "category": "programming_language"},
        {"name": "Java", "category": "programming_language"},
        {"name": "JavaScript", "category": "programming_language"},
        {"name": "HTML/CSS", "category": "web_development"},
        {"name": "SQL", "category": "database"},
        {"name": "NoSQL", "category": "database"},
        {"name": "Flask", "category": "framework"},
        {"name": "Django", "category": "framework"},
        {"name": "Spring", "category": "framework"},
        {"name": "React", "category": "framework"},
        {"name": "Angular", "category": "framework"},
        {"name": "Vue.js", "category": "framework"},
        {"name": "Docker", "category": "devops"},
        {"name": "Kubernetes", "category": "devops"},
        {"name": "Git", "category": "tool"},
        {"name": "Machine Learning", "category": "data_science"},
        {"name": "Data Analysis", "category": "data_science"},
        {"name": "Android Development", "category": "mobile"},
        {"name": "iOS Development", "category": "mobile"},
        {"name": "Cloud Computing", "category": "infrastructure"}
    ]
    
    for skill_data in skills_data:
        skill = Skill.query.filter_by(name=skill_data["name"]).first()
        if not skill:
            skill = Skill(
                name=skill_data["name"],
                category=skill_data["category"]
            )
            db.session.add(skill)
    
    db.session.commit()
    print(f"✓ Seeded {len(skills_data)} skills")

def seed_content():
    """Seed learning content."""
    content_data = [
        {
            "title": "Python for Beginners",
            "description": "Comprehensive introduction to Python programming language.",
            "content_type": "course",
            "difficulty": "beginner",
            "duration_minutes": 480,
            "source_name": "TechLearn Academy",
            "source_url": "https://docs.python.org/3/tutorial/index.html",
            "is_free": True,
            "skills": ["Python"]
        },
        {
            "title": "Advanced Python Programming",
            "description": "Deep dive into advanced Python concepts including decorators, generators, and metaprogramming.",
            "content_type": "course",
            "difficulty": "advanced",
            "duration_minutes": 720,
            "source_name": "TechLearn Academy",
            "source_url": "https://realpython.com/tutorials/advanced/",
            "is_free": False,
            "skills": ["Python"]
        },
        {
            "title": "Python for Data Science",
            "description": "Learn how to use Python for data analysis, visualization, and machine learning.",
            "content_type": "course",
            "difficulty": "intermediate",
            "duration_minutes": 600,
            "source_name": "Data Science Institute",
            "source_url": "https://www.kaggle.com/learn/python",
            "is_free": True,
            "skills": ["Python", "Data Analysis", "Machine Learning"]
        },
        {
            "title": "Building Web Applications with Flask",
            "description": "Create web applications using the Flask microframework.",
            "content_type": "tutorial",
            "difficulty": "intermediate",
            "duration_minutes": 240,
            "source_name": "Web Dev Masters",
            "source_url": "https://flask.palletsprojects.com/en/latest/tutorial/",
            "is_free": True,
            "skills": ["Python", "Flask", "HTML/CSS"]
        },
        {
            "title": "Python Testing and Quality Assurance",
            "description": "Best practices for testing Python applications and ensuring code quality.",
            "content_type": "article",
            "difficulty": "intermediate",
            "duration_minutes": 60,
            "source_name": "QA Experts",
            "source_url": "https://docs.pytest.org/en/latest/getting-started.html",
            "is_free": True,
            "skills": ["Python"]
        },
        {
            "title": "Java Programming Fundamentals",
            "description": "Introduction to Java programming for beginners.",
            "content_type": "course",
            "difficulty": "beginner",
            "duration_minutes": 540,
            "source_name": "Java Learning Center",
            "source_url": "https://dev.java/learn/getting-started/",
            "is_free": True,
            "skills": ["Java"]
        },
        {
            "title": "Advanced Java Development",
            "description": "Advanced Java techniques including multithreading, reflection, and design patterns.",
            "content_type": "course",
            "difficulty": "advanced",
            "duration_minutes": 720,
            "source_name": "Enterprise Java School",
            "source_url": "https://docs.oracle.com/javase/tutorial/java/javaOO/index.html",
            "is_free": False,
            "skills": ["Java"]
        },
        {
            "title": "Android App Development with Java",
            "description": "Build Android applications using Java and Android Studio.",
            "content_type": "course",
            "difficulty": "intermediate",
            "duration_minutes": 840,
            "source_name": "Mobile Dev Academy",
            "source_url": "https://developer.android.com/courses",
            "is_free": True,
            "skills": ["Java", "Android Development"]
        },
        {
            "title": "Spring Framework Masterclass",
            "description": "Comprehensive guide to building enterprise applications with Spring Framework.",
            "content_type": "course",
            "difficulty": "advanced",
            "duration_minutes": 960,
            "source_name": "Enterprise Solutions",
            "source_url": "https://spring.io/guides/tutorials/rest/",
            "is_free": False,
            "skills": ["Java", "Spring"]
        },
        {
            "title": "Java Database Connectivity",
            "description": "Learn how to connect Java applications to databases using JDBC.",
            "content_type": "tutorial",
            "difficulty": "intermediate",
            "duration_minutes": 180,
            "source_name": "Data Systems Inc",
            "source_url": "https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html",
            "is_free": True,
            "skills": ["Java", "SQL"]
        },
        {
            "title": "Python vs Java: Which Should You Learn First?",
            "description": "Comparison of Python and Java for beginners deciding which language to learn.",
            "content_type": "article",
            "difficulty": "beginner",
            "duration_minutes": 20,
            "source_name": "Programming Insights",
            "source_url": "https://realpython.com/python-vs-java/",
            "is_free": True,
            "skills": ["Python", "Java"]
        },
        {
            "title": "Building RESTful APIs with Python and Flask",
            "description": "Tutorial on building REST APIs using Flask.",
            "content_type": "tutorial",
            "difficulty": "intermediate",
            "duration_minutes": 150,
            "source_name": "API Masters",
            "source_url": "https://flask.palletsprojects.com/en/latest/tutorial/views/",
            "is_free": True,
            "skills": ["Python", "Flask"]
        },
        {
            "title": "Java Concurrency: Understanding Threads and ThreadPools",
            "description": "In-depth guide to multithreading in Java.",
            "content_type": "article",
            "difficulty": "advanced",
            "duration_minutes": 90,
            "source_name": "Java Magazine",
            "source_url": "https://docs.oracle.com/javase/tutorial/essential/concurrency/index.html",
            "is_free": True,
            "skills": ["Java"]
        },
        {
            "title": "Python for Machine Learning: Scikit-Learn Tutorial",
            "description": "Introduction to machine learning with Python's scikit-learn library.",
            "content_type": "tutorial",
            "difficulty": "intermediate",
            "duration_minutes": 240,
            "source_name": "ML Academy",
            "source_url": "https://scikit-learn.org/stable/tutorial/index.html",
            "is_free": True,
            "skills": ["Python", "Machine Learning"]
        },
        {
            "title": "Java Performance Tuning and Optimization",
            "description": "Techniques for improving Java application performance.",
            "content_type": "course",
            "difficulty": "advanced",
            "duration_minutes": 420,
            "source_name": "Performance Masters",
            "source_url": "https://www.oracle.com/java/technologies/performance-tuning.html",
            "is_free": False,
            "skills": ["Java"]
        }
    ]
    
    for content_data in content_data:
        content = Content.query.filter_by(title=content_data["title"]).first()
        if not content:
            content = Content(
                title=content_data["title"],
                description=content_data["description"],
                content_type=content_data["content_type"],
                difficulty=content_data["difficulty"],
                duration_minutes=content_data["duration_minutes"],
                source_name=content_data["source_name"],
                source_url=content_data["source_url"],
                is_free=content_data["is_free"],
                created_at=datetime.utcnow()
            )
            
            # Add skills
            for skill_name in content_data["skills"]:
                skill = Skill.query.filter_by(name=skill_name).first()
                if skill:
                    content.skills.append(skill)
            
            db.session.add(content)
    
    db.session.commit()
    print(f"✓ Seeded {len(content_data)} content items")

def seed_events():
    """Seed tech events."""
    now = datetime.utcnow()
    events_data = [
        {
            "title": "Python Developer Conference Chennai",
            "description": "Annual conference for Python developers in Chennai featuring talks, workshops, and networking opportunities.",
            "event_type": "conference",
            "is_online": False,
            "location": "Chennai Trade Center, Chennai",
            "start_datetime": now + timedelta(days=30),
            "end_datetime": now + timedelta(days=32),
            "registration_url": "https://www.meetup.com/pythonchennai/",
            "organizer": "Python Chennai User Group",
            "skills": ["Python", "Flask", "Django"]
        },
        {
            "title": "Java Enterprise Solutions Summit",
            "description": "Summit focused on Java enterprise development, cloud solutions, and microservices architecture.",
            "event_type": "summit",
            "is_online": False,
            "location": "ITC Grand Chola, Chennai",
            "start_datetime": now + timedelta(days=45),
            "end_datetime": now + timedelta(days=46),
            "registration_url": "https://events.oracle.com/java/",
            "organizer": "Oracle India",
            "skills": ["Java", "Spring"]
        },
        {
            "title": "TechLearn Workshop: Machine Learning with Python",
            "description": "Hands-on workshop on implementing machine learning algorithms using Python and scikit-learn.",
            "event_type": "workshop",
            "is_online": False,
            "location": "Anna University, Chennai",
            "start_datetime": now + timedelta(days=15),
            "end_datetime": now + timedelta(days=15) + timedelta(hours=8),
            "registration_url": "https://www.tensorflow.org/community/events",
            "organizer": "TechLearn and Anna University",
            "skills": ["Python", "Machine Learning", "Data Analysis"]
        },
        {
            "title": "Chennai DevFest 2025",
            "description": "Google Developer Group's annual DevFest covering Android, Web, Cloud, and AI technologies.",
            "event_type": "festival",
            "is_online": False,
            "location": "Chennai Convention Centre, Chennai",
            "start_datetime": now + timedelta(days=90),
            "end_datetime": now + timedelta(days=91),
            "registration_url": "https://developers.google.com/events",
            "organizer": "Google Developer Group Chennai",
            "skills": ["Android Development", "Cloud Computing", "Machine Learning"]
        },
        {
            "title": "Web Development Bootcamp",
            "description": "Intensive 2-day bootcamp covering modern web development technologies and practices.",
            "event_type": "bootcamp",
            "is_online": False,
            "location": "Ramada Plaza, Chennai",
            "start_datetime": now + timedelta(days=21),
            "end_datetime": now + timedelta(days=22),
            "registration_url": "https://frontendmasters.com/learn/",
            "organizer": "CodeCraft Academy",
            "skills": ["HTML/CSS", "JavaScript", "React"]
        },
        {
            "title": "Virtual Python Conference 2025",
            "description": "Online conference featuring Python experts from around the world discussing the latest trends and techniques.",
            "event_type": "conference",
            "is_online": True,
            "location": "Online",
            "start_datetime": now + timedelta(days=60),
            "end_datetime": now + timedelta(days=62),
            "registration_url": "https://us.pycon.org/2025/",
            "organizer": "Python Software Foundation",
            "skills": ["Python", "Django", "Flask", "Data Analysis"]
        },
        {
            "title": "Java Performance Tuning Webinar",
            "description": "Online webinar on optimizing Java application performance in production environments.",
            "event_type": "webinar",
            "is_online": True,
            "location": "Online",
            "start_datetime": now + timedelta(days=7),
            "end_datetime": now + timedelta(days=7) + timedelta(hours=2),
            "registration_url": "https://inside.java/events/",
            "organizer": "Java Champions",
            "skills": ["Java"]
        },
        {
            "title": "Data Science with Python: Online Workshop",
            "description": "Interactive online workshop on data analysis and visualization using Python libraries.",
            "event_type": "workshop",
            "is_online": True,
            "location": "Online",
            "start_datetime": now + timedelta(days=14),
            "end_datetime": now + timedelta(days=14) + timedelta(hours=4),
            "registration_url": "https://www.anaconda.com/events",
            "organizer": "Anaconda Inc.",
            "skills": ["Python", "Data Analysis"]
        }
    ]
    
    for event_data in events_data:
        event = Event.query.filter_by(title=event_data["title"]).first()
        if not event:
            event = Event(
                title=event_data["title"],
                description=event_data["description"],
                event_type=event_data["event_type"],
                is_online=event_data["is_online"],
                location=event_data["location"],
                start_datetime=event_data["start_datetime"],
                end_datetime=event_data["end_datetime"],
                registration_url=event_data["registration_url"],
                organizer=event_data["organizer"],
                created_at=datetime.utcnow()
            )
            
            # Add skills
            for skill_name in event_data["skills"]:
                skill = Skill.query.filter_by(name=skill_name).first()
                if skill:
                    event.skills.append(skill)
            
            db.session.add(event)
    
    db.session.commit()
    print(f"✓ Seeded {len(events_data)} events")

def seed_roadmaps():
    """Seed learning roadmaps."""
    roadmaps_data = [
        {
            "title": "Python Developer Roadmap",
            "description": "Comprehensive learning path to become a proficient Python developer, covering fundamentals to advanced concepts.",
            "difficulty": "beginner",
            "estimated_hours": 120,
            "skills": ["Python", "Flask", "Django", "SQL"],
            "topics": [
                {
                    "title": "Python Fundamentals",
                    "description": "Core Python concepts and syntax",
                    "order": 1,
                    "resources": [
                        {"title": "Python Official Documentation", "url": "https://docs.python.org/3/"},
                        {"title": "Learn Python - Full Course for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"}
                    ]
                },
                {
                    "title": "Python Advanced Concepts",
                    "description": "Advanced topics including decorators, generators, and OOP",
                    "order": 2,
                    "resources": [
                        {"title": "Python Design Patterns", "url": "https://refactoring.guru/design-patterns/python"},
                        {"title": "Real Python - Advanced Python Features", "url": "https://realpython.com/"}
                    ]
                },
                {
                    "title": "Web Development with Python",
                    "description": "Building web applications using Python frameworks",
                    "order": 3,
                    "resources": [
                        {"title": "Flask Official Documentation", "url": "https://flask.palletsprojects.com/"},
                        {"title": "Django Tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/"}
                    ]
                },
                {
                    "title": "Data Science with Python",
                    "description": "Using Python for data analysis and machine learning",
                    "order": 4,
                    "resources": [
                        {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"}
                    ]
                },
                {
                    "title": "Python Testing and Best Practices",
                    "description": "Testing frameworks and code quality",
                    "order": 5,
                    "resources": [
                        {"title": "Python Testing with pytest", "url": "https://docs.pytest.org/en/latest/"},
                        {"title": "Clean Code in Python", "url": "https://github.com/zedr/clean-code-python"}
                    ]
                },
                {
                    "title": "Python Developer Tools",
                    "description": "Essential tools for Python development",
                    "order": 6,
                    "resources": [
                        {"title": "Visual Studio Code for Python", "url": "https://code.visualstudio.com/docs/languages/python"},
                        {"title": "PyCharm Tutorial", "url": "https://www.jetbrains.com/help/pycharm/quick-start-guide.html"},
                        {"title": "Git and GitHub for Python Developers", "url": "https://realpython.com/python-git-github-intro/"}
                    ]
                }
            ]
        },
        {
            "title": "Java Developer Roadmap",
            "description": "Structured learning path for becoming a professional Java developer, from basics to enterprise applications.",
            "difficulty": "beginner",
            "estimated_hours": 150,
            "skills": ["Java", "Spring", "SQL"],
            "topics": [
                {
                    "title": "Java Foundations",
                    "description": "Core Java concepts and syntax",
                    "order": 1,
                    "resources": [
                        {"title": "Java Tutorial for Beginners", "url": "https://docs.oracle.com/javase/tutorial/"},
                        {"title": "Java Programming Masterclass", "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/"}
                    ]
                },
                {
                    "title": "Object-Oriented Programming in Java",
                    "description": "OOP principles and design patterns",
                    "order": 2,
                    "resources": [
                        {"title": "Object-Oriented Programming in Java", "url": "https://www.coursera.org/learn/object-oriented-java"},
                        {"title": "Head First Design Patterns", "url": "https://www.oreilly.com/library/view/head-first-design/0596007124/"}
                    ]
                },
                {
                    "title": "Java Advanced Features",
                    "description": "Advanced Java concepts",
                    "order": 3,
                    "resources": [
                        {"title": "Java Generics and Collections", "url": "https://www.oracle.com/technical-resources/articles/java/generics.html"}
                    ]
                },
                {
                    "title": "Spring Framework",
                    "description": "Enterprise Java development with Spring",
                    "order": 4,
                    "resources": [
                        {"title": "Spring Framework Documentation", "url": "https://spring.io/projects/spring-framework"},
                        {"title": "Spring Boot in Action", "url": "https://www.manning.com/books/spring-boot-in-action"},
                        {"title": "Building REST APIs with Spring", "url": "https://spring.io/guides/tutorials/rest/"}
                    ]
                }
            ]
        },
        {
            "title": "Data Science Learning Path",
            "description": "Comprehensive roadmap for becoming a data scientist, covering statistics, programming, and machine learning.",
            "difficulty": "intermediate",
            "estimated_hours": 200,
            "skills": ["Python", "Data Analysis", "Machine Learning"],
            "topics": [
                {
                    "title": "Foundations of Data Science",
                    "description": "Core concepts in statistics and programming",
                    "order": 1,
                    "resources": [
                        {"title": "Introduction to Statistical Learning", "url": "https://www.statlearning.com/"},
                        {"title": "Python for Data Analysis", "url": "https://wesmckinney.com/book/"}
                    ]
                },
                {
                    "title": "Data Manipulation and Visualization",
                    "description": "Tools and techniques for working with data",
                    "order": 2,
                    "resources": [
                        {"title": "Pandas Documentation", "url": "https://pandas.pydata.org/docs/"},
                        {"title": "Data Visualization with Matplotlib and Seaborn", "url": "https://matplotlib.org/"}
                    ]
                },
                {
                    "title": "Machine Learning Fundamentals",
                    "description": "Core machine learning algorithms and concepts",
                    "order": 3,
                    "resources": [
                        {"title": "Scikit-Learn Documentation", "url": "https://scikit-learn.org/stable/"},
                        {"title": "Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"}
                    ]
                },
                {
                    "title": "Deep Learning",
                    "description": "Neural networks and deep learning techniques",
                    "order": 4,
                    "resources": [
                        {"title": "Deep Learning with Python", "url": "https://www.manning.com/books/deep-learning-with-python"},
                        {"title": "TensorFlow Documentation", "url": "https://www.tensorflow.org/learn"}
                    ]
                },
                {
                    "title": "Data Science Projects",
                    "description": "Real-world applications and portfolio building",
                    "order": 5,
                    "resources": [
                        {"title": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions"}
                    ]
                }
            ]
        },
        {
            "title": "Android Development Path",
            "description": "Comprehensive guide to becoming an Android developer, from Java basics to publishing apps.",
            "difficulty": "intermediate",
            "estimated_hours": 160,
            "skills": ["Java", "Android Development"],
            "topics": [
                {
                    "title": "Java for Android",
                    "description": "Essential Java concepts for Android development",
                    "order": 1,
                    "resources": [
                        {"title": "Java Programming for Android Developers", "url": "https://developer.android.com/codelabs/build-your-first-android-app"},
                        {"title": "Java Essentials for Android", "url": "https://www.udacity.com/course/java-for-android--ud843"}
                    ]
                },
                {
                    "title": "Android Fundamentals",
                    "description": "Core Android concepts and components",
                    "order": 2,
                    "resources": [
                        {"title": "Android Developer Fundamentals", "url": "https://developer.android.com/courses/fundamentals-training/overview-v2"},
                        {"title": "Android Studio Essentials", "url": "https://developer.android.com/studio/intro"}
                    ]
                },
                {
                    "title": "Android UI Development",
                    "description": "Creating user interfaces for Android",
                    "order": 3,
                    "resources": [
                        {"title": "Material Design for Android", "url": "https://material.io/develop/android"},
                        {"title": "Android Layout and Views", "url": "https://developer.android.com/guide/topics/ui/declaring-layout"}
                    ]
                },
                {
                    "title": "Android Data and Storage",
                    "description": "Working with data in Android applications",
                    "order": 4,
                    "resources": [
                        {"title": "Room Persistence Library", "url": "https://developer.android.com/training/data-storage/room"},
                        {"title": "Android Networking", "url": "https://developer.android.com/training/volley"}
                    ]
                },
                {
                    "title": "Advanced Android Development",
                    "description": "Advanced topics in Android",
                    "order": 5,
                    "resources": [
                        {"title": "Android Architecture Components", "url": "https://developer.android.com/topic/libraries/architecture"},
                        {"title": "Android Performance", "url": "https://developer.android.com/topic/performance"}
                    ]
                },
                {
                    "title": "Publishing Android Apps",
                    "description": "Preparing and publishing to Google Play",
                    "order": 6,
                    "resources": [
                        {"title": "Google Play Console", "url": "https://developer.android.com/distribute/console"},
                        {"title": "App Release Process", "url": "https://developer.android.com/studio/publish"}
                    ]
                }
            ]
        }
    ]
    
    for roadmap_data in roadmap_data:
        roadmap = Roadmap.query.filter_by(title=roadmap_data["title"]).first()
        if not roadmap:
            roadmap = Roadmap(
                title=roadmap_data["title"],
                description=roadmap_data["description"],
                difficulty=roadmap_data["difficulty"],
                estimated_hours=roadmap_data["estimated_hours"],
                created_at=datetime.utcnow()
            )
            
            # Add skills
            for skill_name in roadmap_data["skills"]:
                skill = Skill.query.filter_by(name=skill_name).first()
                if skill:
                    roadmap.skills.append(skill)
            
            db.session.add(roadmap)
            db.session.flush()  # Ensure roadmap has ID before adding topics
            
            # Add topics
            for topic_data in roadmap_data["topics"]:
                topic = RoadmapTopic(
                    roadmap_id=roadmap.id,
                    title=topic_data["title"],
                    description=topic_data["description"],
                    order=topic_data["order"]
                )
                db.session.add(topic)
                db.session.flush()  # Ensure topic has ID before adding resources
                
                # Add resources
                for resource_data in topic_data.get("resources", []):
                    resource = RoadmapResource(
                        topic_id=topic.id,
                        title=resource_data["title"],
                        url=resource_data.get("url")
                    )
                    db.session.add(resource)
    
    db.session.commit()
    print(f"✓ Seeded {len(roadmaps_data)} roadmaps")

def seed_admin_user():
    """Create an admin user for initial access."""
    admin = User.query.filter_by(email="admin@techlearn.com").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@techlearn.com",
            password_hash=generate_password_hash("TechLearn@Admin123"),
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Created admin user (admin@techlearn.com / TechLearn@Admin123)")
    else:
        print("✓ Admin user already exists")

def main():
    """Run all seed functions."""
    app = create_app()
    with app.app_context():
        print("========================================")
        print("TechLearn Database Seeding")
        print("========================================")
        
        seed_skills()
        seed_content()
        seed_events()
        seed_roadmaps()
        seed_admin_user()
        
        print("\n========================================")
        print("Database seeding complete!")
        print("========================================")

if __name__ == "__main__":
    main()