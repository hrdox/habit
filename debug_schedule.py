from app import app, db, User, Schedule, RoutineItem
from datetime import datetime

with app.app_context():
    client = app.test_client()
    
    # 1. Setup User
    user = User.query.filter_by(username='admin').first()
    if not user:
        print("Admin missing?")
        exit()
        
    client.post('/login', data={'username': 'admin', 'password': 'adminpass'}, follow_redirects=True)
    
    # 2. Check/Reset Schedule
    s = Schedule.query.filter_by(user_id=user.id, is_active=True).first()
    if s:
        print(f"Found active schedule: {s.name}")
        # Clear items to test fresh add
        RoutineItem.query.filter_by(schedule_id=s.id).delete()
        db.session.commit()
    else:
        print("No active schedule, creating one via API...")
        # Simulate form post
        client.post('/schedule', data={'schedule_name': 'Test Schedule'})
        s = Schedule.query.filter_by(user_id=user.id, is_active=True).first()
        print(f"Created: {s.name}")

    # 3. Add Routine Item (For Sunday)
    today_name = datetime.utcnow().strftime('%A') # This might differ from user local time!
    # User local time is Sunday (2026-01-04). 
    # UTC now? User meta says local is 22:13 +06:00. 
    # So UTC is ~16:13. Still Sunday.
    target_day = "Sunday" 
    
    print(f"Adding routine for {target_day}...")
    resp = client.post('/schedule', data={
        'title': 'Debug Class',
        'day': target_day,
        'start_time': '10:00',
        'end_time': '11:00',
        'location': 'Room 101'
    }, follow_redirects=True)
    
    if resp.status_code != 200:
        print(f"Add Routine Failed: {resp.status_code}")
    
    # Check DB
    item = RoutineItem.query.filter_by(schedule_id=s.id, title='Debug Class').first()
    if item:
        print(f"SUCCESS: Routine '{item.title}' saved for {item.day_of_week}.")
    else:
        print("FAILURE: Routine not saved in DB.")
        
    # 4. Check Dashboard
    print("Checking Dashboard...")
    resp = client.get('/dashboard')
    html = resp.get_data(as_text=True)
    if 'Debug Class' in html:
        print("SUCCESS: Routine visible on Dashboard.")
    else:
        print("FAILURE: Routine NOT visible on Dashboard.")
        # Debug why
        # Check today in app context vs target_day
        # We can't easily hook into the view's 'today' var without modifying app, 
        # but we know app uses date.today().
        print(f"HTML Snippet around Schedule: {html[html.find('Today'):html.find('Today')+500]}...")
