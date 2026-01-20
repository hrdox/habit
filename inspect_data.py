from app import app, User, Schedule, RoutineItem, db
from sqlalchemy import text

with app.app_context():
    # Inspect admin user's schedules
    user = User.query.filter_by(username='admin').first()
    if not user:
        print("Admin user not found.")
    else:
        print(f"User: {user.username} (ID: {user.id})")
        
        schedules = Schedule.query.filter_by(user_id=user.id).all()
        print(f"Found {len(schedules)} schedules.")
        
        for s in schedules:
            print(f" - ID: {s.id} | Name: {s.name} | Active: {s.is_active}")
            items = RoutineItem.query.filter_by(schedule_id=s.id).all()
            print(f"   Items ({len(items)}):")
            for i in items:
                print(f"     * {i.day_of_week}: {i.title} ({i.start_time} - {i.end_time})")

        # Check today's routines query logic
        from datetime import date
        today = date.today()
        day_name = today.strftime('%A')
        print(f"\nServer Today: {today} ({day_name})")
