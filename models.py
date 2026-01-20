from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user', 'admin'
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    habits = db.relationship('Habit', backref='owner', lazy=True)
    schedules = db.relationship('Schedule', backref='owner', lazy=True)
    prayer_logs = db.relationship('PrayerLog', backref='user', lazy=True)
    days = db.relationship('Day', backref='user', lazy=True)
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default='General') # Health, Study, Spirit, etc.
    frequency = db.Column(db.String(20), default='Daily') # Daily, Weekly
    target_quantity = db.Column(db.Integer, default=1) # For quantity habits
    unit = db.Column(db.String(20), nullable=True) # e.g., 'pages', 'minutes'
    points = db.Column(db.Integer, default=10) # Points awarded for completion
    
    # V2 Fields
    priority = db.Column(db.Integer, default=3) # 1-5
    min_value = db.Column(db.Integer, default=1) # Minimum effort to count as "done"
    target_value = db.Column(db.Integer, default=1) # Full target
    # unit already exists
    identity_label = db.Column(db.String(100), nullable=True) # "I am a reader"
    difficulty = db.Column(db.Integer, default=1) # 1-10, auto-adjust later

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_paused = db.Column(db.Boolean, default=False)
    
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade="all, delete-orphan")

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=False)
    value_done = db.Column(db.Integer, default=0) # renaming value_current conceptually or aliasing
    quality = db.Column(db.Integer, default=2) # 1-3 (Poor, Avg, Good)
    points = db.Column(db.Integer, default=0) # Calculated points for this specific log
    
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g. "Spring Semester"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    items = db.relationship('RoutineItem', backref='schedule', lazy=True, cascade="all, delete-orphan")

class RoutineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False) # Class Name
    day_of_week = db.Column(db.String(10), nullable=False) # Monday, Tuesday...
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    
class ScheduleLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine_item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Denormalized for easier query
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=10)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=True)

class PrayerLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    fajr = db.Column(db.Boolean, default=False)
    dhuhr = db.Column(db.Boolean, default=False)
    asr = db.Column(db.Boolean, default=False)
    maghrib = db.Column(db.Boolean, default=False)
    isha = db.Column(db.Boolean, default=False)
    
    # Optional dedicated points for the day
    spiritual_score = db.Column(db.Integer, default=0)

class Dua(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Null if system default
    title = db.Column(db.String(100), nullable=False)
    arabic_text = db.Column(db.Text, nullable=True)
    english_meaning = db.Column(db.Text, nullable=True)
    bangla_meaning = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='General') # Morning, Evening, etc.

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    intention = db.Column(db.String(255), nullable=True)
    energy_level = db.Column(db.Integer, default=3) # 1-5
    mood = db.Column(db.Integer, default=3) # 1-5
    reflection = db.Column(db.Text, nullable=True)
    total_score = db.Column(db.Integer, default=0)
    
    # Relationships
    habit_logs = db.relationship('HabitLog', backref='day', lazy=True)
    prayer_logs = db.relationship('PrayerLog', backref='day', lazy=True)
    schedule_logs = db.relationship('ScheduleLog', backref='day', lazy=True)
