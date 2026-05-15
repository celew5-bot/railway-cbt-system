from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    zone = db.Column(db.String(50))
    division = db.Column(db.String(50))
    lobby = db.Column(db.String(50))
    
    # user_type can be: superadmin, zonal_superadmin, division_admin, admin
    user_type = db.Column(db.String(20), nullable=False) 
    status = db.Column(db.String(20), default='active')
    created_by = db.Column(db.Integer)
    last_login = db.Column(db.DateTime)

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.String(50), unique=True, nullable=False)
    candidate_name = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50))
    division = db.Column(db.String(50))
    lobby = db.Column(db.String(50))
    post = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15), nullable=False)
    test_status = db.Column(db.String(20), default='not_started')
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    test_number = db.Column(db.Integer, nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    test_description = db.Column(db.Text)
    max_score = db.Column(db.Float, nullable=False)
    passing_percentage = db.Column(db.Float, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='active')

class TestAttempt(db.Model):
    __tablename__ = 'candidate_test_attempts'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    lobby_id = db.Column(db.String(50))
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    percentage = db.Column(db.Float)
    result = db.Column(db.String(10))
    time_taken = db.Column(db.Integer)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_type = db.Column(db.String(20))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)