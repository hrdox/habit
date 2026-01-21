from app import app, db, User
with app.app_context():
    # Promote 'admin' to 'super_admin' or create 'superadmin'
    super_user = User.query.filter_by(username='superadmin').first()
    if not super_user:
        super_user = User(username='superadmin', email='superadmin@habit.local', role='super_admin')
        super_user.set_password('superpass')
        db.session.add(super_user)
        db.session.commit()
        print("Created superadmin user!")
    else:
        print("superadmin already exists.")
