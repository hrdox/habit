import unittest
from app import app, db, User, Habit, Schedule, RoutineItem
from datetime import date, time

class HabitTrackerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create Test User
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        
        # Create Another User (for auth checks)
        self.other_user = User(username='other', email='other@example.com')
        self.other_user.set_password('password')
        db.session.add(self.other_user)
        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('testuser', 'password')
        self.assertIn(b'Dashboard', rv.data or rv.response) # Adjust based on actual response content
        rv = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', rv.data)

    def test_habit_creation_and_toggle(self):
        self.login('testuser', 'password')
        
        # Add Habit
        rv = self.app.post('/habit/add', data=dict(
            name='Test Habit',
            category='General',
            frequency='Daily'
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        
        habit = Habit.query.filter_by(name='Test Habit').first()
        self.assertIsNotNone(habit)
        
        # Toggle Habit
        rv = self.app.post(f'/habit/toggle/{habit.id}')
        self.assertEqual(rv.status_code, 200)
        json_data = rv.get_json()
        self.assertTrue(json_data['success'])
        self.assertTrue(json_data['new_status'])

    def test_habit_with_site_url(self):
        self.login('testuser', 'password')
        
        # Add Habit with URL
        url = "https://www.example.com"
        rv = self.app.post('/habit/add', data=dict(
            name='Link Habit',
            category='Study',
            frequency='Daily',
            site_url=url
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        
        habit = Habit.query.filter_by(name='Link Habit').first()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.site_url, url)
        
        # Test Edit URL
        new_url = "https://www.google.com"
        rv = self.app.post(f'/habit/edit/{habit.id}', data=dict(
            name='Link Habit',
            category='Study',
            frequency='Daily',
            site_url=new_url,
            priority=habit.priority,
            difficulty=habit.difficulty,
            target_value=habit.target_value,
            min_value=habit.min_value,
            unit=habit.unit
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        
        db.session.refresh(habit)
        self.assertEqual(habit.site_url, new_url)

    def test_unauthorized_habit_toggle(self):
        # Login as other user
        self.login('other', 'password')
        
        # Create habit for first user
        habit = Habit(name='User1 Habit', user_id=self.user.id)
        db.session.add(habit)
        db.session.commit()
        
        # Try to toggle
        rv = self.app.post(f'/habit/toggle/{habit.id}')
        self.assertEqual(rv.status_code, 403)
        self.assertFalse(rv.get_json()['success'])

    def test_schedule_flow(self):
        self.login('testuser', 'password')
        
        # Create Schedule
        rv = self.app.post('/schedule', data=dict(
            schedule_name='Spring 2025'
        ), follow_redirects=True)
        
        schedule = Schedule.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(schedule)
        
        # Add Routine
        rv = self.app.post('/schedule', data=dict(
            title='Math 101',
            day='Monday',
            start_time='10:00',
            end_time='11:00',
            location='Room 101'
        ), follow_redirects=True)
        
        item = RoutineItem.query.filter_by(title='Math 101').first()
        self.assertIsNotNone(item)
        
        # Toggle Routine

if __name__ == '__main__':
    unittest.main()
