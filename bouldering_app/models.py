from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, CheckConstraint
from . import db 

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(String, nullable=False)
    profile_picture = Column(String)
    highest_grade_climbed = Column(Integer, default=0)
    highest_grade_flased = Column(Integer, default=0)

    boulders = db.relationship('Boulder', back_populates='creator')
    attempts = db.relationship('Attempt', back_populates='user')

class Boulder(db.Model):
    __tablename__ = 'boulder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    numberofmoves = Column(Integer, nullable=False)
    set_date = Column(Date)
    description = Column(Text)
    image = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)

    creator = db.relationship('User', back_populates='boulders')
    attempts = db.relationship('Attempt', back_populates='boulder')

class Attempt(db.Model):
    __tablename__ = 'attempt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_of_attempts = Column(Integer, nullable=False)
    status = Column(String, CheckConstraint("status IN ('incomplete', 'completed', 'flashed')"), nullable=False)
    attempt_date = Column(Date, default='CURRENT_DATE')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    boulder_id = Column(Integer, ForeignKey('boulder.id'), nullable=False)
    moves_completed = Column(Integer)
    difficulty = Column(Integer, nullable=False)

    user = db.relationship('User', back_populates='attempts')
    boulder = db.relationship('Boulder', back_populates='attempts')
