# TechLearn - Comprehensive Learning Platform

TechLearn is a comprehensive Flask-based learning platform designed to streamline educational content discovery, tracking, and engagement. The platform is organized into three key modules: Collect (content management), Connect (event management), and Crux (structured learning paths).

![TechLearn Platform](static/img/techlearn-preview.png)

## Features

- **User Authentication System**: Secure registration, login, profile management, and password reset functionality
- **Content Management (Collect)**: Curated learning resources with filtering by skills, difficulty, content type
- **Event Management (Connect)**: Tech events with location-based filtering and registration
- **Learning Paths (Crux)**: Structured roadmaps for Python, Java, Data Science, and Android development
- **Progress Tracking**: Track completion of learning modules and topics
- **Bookmarking System**: Save and organize favorite content and events
- **Assessment Quizzes**: Test knowledge with interactive quizzes

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: PostgreSQL
- **Frontend**: Bootstrap, jQuery, Font Awesome
- **Email**: SendGrid integration

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/techlearn.git
   cd techlearn
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/techlearn
   SESSION_SECRET=your_secret_key_here
   SENDGRID_API_KEY=optional_for_email_functionality
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

7. Access the application at `http://127.0.0.1:5000`

## Project Structure

```
techlearn/
├── app.py                 # Application factory and configuration
├── config.py              # Configuration settings
├── forms.py               # Form definitions using Flask-WTF
├── main.py                # Application entry point
├── models.py              # Database models
├── utils.py               # Utility functions
├── routes/                # Route blueprints
│   ├── auth.py            # Authentication routes
│   ├── collect.py         # Content management routes
│   ├── connect.py         # Event management routes
│   ├── crux.py            # Learning paths routes
│   └── main.py            # Main routes
├── static/                # Static assets
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   └── img/               # Images
└── templates/             # Jinja2 templates
    ├── auth/              # Authentication templates
    ├── collect/           # Content templates
    ├── connect/           # Event templates
    ├── crux/              # Learning paths templates
    └── includes/          # Reusable template parts
```

## Deployment

This application can be deployed to various platforms:

- **Heroku**: Supports PostgreSQL and Python applications
- **Render**: Has free tier with PostgreSQL support
- **PythonAnywhere**: Specifically designed for Python web applications
- **Replit**: Can be deployed directly from development environment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for UI components
- Flask and its extensions for the backend framework
- All the educational resources linked in the platform