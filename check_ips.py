from app import app, db
from models import AuditLog

with app.app_context():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    print(f"{'ID':<5} | {'Action':<15} | {'IP Address':<20} | {'Timestamp'}")
    print("-" * 60)
    for log in logs:
        print(f"{log.id:<5} | {log.action:<15} | {str(log.ip_address):<20} | {log.timestamp}")
