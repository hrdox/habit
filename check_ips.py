from app import app, db
from models import AuditLog

with app.app_context():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    print(f"{'ID':<5} | {'Action':<15} | {'Public IP':<15} | {'Local IP':<15} | {'Timestamp'}")
    print("-" * 80)
    for log in logs:
        print(f"{log.id:<5} | {log.action:<15} | {str(log.ip_address):<15} | {str(log.local_ip):<15} | {log.timestamp}")
