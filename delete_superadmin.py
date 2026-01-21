from app import app, db, User
with app.app_context():
    super_user = User.query.filter_by(username='superadmin').first()
    if super_user:
        db.session.delete(super_user)
        db.session.commit()
        print("Deleted superadmin user.")
    else:
        print("superadmin user not found.")
