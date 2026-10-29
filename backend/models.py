from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='employee')  # 'admin' or 'employee'

    def __repr__(self):
        return f"<User {self.full_name} ({self.email})>"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'in-progress', 'completed'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    assigned_date = db.Column(db.DateTime, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Task {self.title} (Assigned to: {self.assigned_to})>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "assigned_date": self.assigned_date.isoformat() if self.assigned_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None
        }