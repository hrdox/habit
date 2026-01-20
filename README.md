# Habit & Deen Tracker

A comprehensive Flask-based web application to track habits, manage academic schedules, and maintain spiritual routines (Salah & Dua).

## Features
- **Habit Tracking**: Create, view, and toggle daily habits with streak monitoring.
- **Schedule Management**: Organize classes and routines; view them in a calendar or list format.
- **Prayer & Deen**: Log daily prayers (Salah) and calculate a daily "Spiritual Score". View and read Duas.
- **Analytics**: Visualize your progress over the last 30 days with interactive charts.
- **Dynamic UI**: Modern, responsive interface with Dark Mode support and glassmorphism design.
- **OCR Import**: Upload schedule images to extract text (requires Tesseract).

## Technology Stack
- **Backend**: Python, Flask, SQLAlchemy, Flask-Login.
- **Frontend**: HTML5, CSS3 (Custom Modern Design), JavaScript (Vanilla).
- **Database**: SQLite (local).

## Setup Instructions

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: For OCR features, ensure [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) is installed on your system.*

2.  **Initialize Database**
    Run the app once, and it will auto-create `instance/habit.db` (or run `python -c "from app import app, db; app.app_context().push(); db.create_all()"`).
    
    *Optional: To fix/reset DB structure, check `fix_db_v2.py`.*

3.  **Run the Application**
    ```bash
    python app.py
    ```
    Access the app at `http://127.0.0.1:5000`.

## Testing
To run the automated test suite (checking auth, habits, and schedule logic):
```bash
python test_app.py
```
    
## Usage
- **Register/Login**: Create an account to start tracking.
- **Dashboard**: Your central hub for today's tasks and prayers.
- **Calendar**: View your upcoming schedule.
- **Dark Mode**: Toggle via the moon icon in the top right.
