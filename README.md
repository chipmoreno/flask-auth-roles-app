# Flask Auth Roles App

A simple Flask web application demonstrating user authentication, registration, and role-based access control (admin/user) using Flask-Login and SQLAlchemy.

## Features

- User registration and login
- Password hashing
- Role-based access (admin and user)
- Admin panel (admin only)
- User profile page
- Flash messages for feedback

## Requirements

- Python 3.7+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- WTForms

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flask-auth-roles-app.git
   cd flask-auth-roles-app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

## Usage

- Register a new user at `/register`
- Log in at `/login`
- Access your profile at `/profile`
- If your user has the `admin` role, access the admin panel at `/admin`

## Project Structure

```
my_flask_app3/
│
├── app.py
├── models.py
├── forms.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   └── admin.html
└── .gitignore
```

## Notes

- The database is SQLite (`auth_app.db`) by default.
- The first time you run the app, default roles (`admin`, `user`) are created.
- The `venv/` directory is excluded from git via `.gitignore`.

##
